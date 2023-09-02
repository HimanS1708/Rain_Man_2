import math
from scipy.optimize import minimize
from functools import cmp_to_key
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def str(self):
        return f"({self.x}, {self.y})"
    def conj(self):
        return Point(self.x,-self.y)
    def dot(self, other):
        """Calculate the dot product of two points."""
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        """Calculate the cross product of two points."""
        return self.x * other.y - self.y * other.x

    def scalar_multiply(self, scalar):
        """Multiply the point by a scalar."""
        return Point(self.x * scalar, self.y * scalar)

    def rotate(self, angle_degrees):
        """Rotate the point by a given angle in degrees."""
        angle_radians = math.radians(angle_degrees)
        new_x = self.x * math.cos(angle_radians) - self.y * math.sin(angle_radians)
        new_y = self.x * math.sin(angle_radians) + self.y * math.cos(angle_radians)
        return Point(new_x, new_y)
    def __add__(self , other):
        return Point(self.x+other.x, self.y+other.y)
    def __neg__(self):
        return Point(-self.x, -self.y)
    def __sub__(self,other):
        return Point(self.x-other.x, self.y-other.y)
    def __mul__(self, other):
        """Support * operator for both scalar and point * point multiplication."""
        if isinstance(other, (int, float)):
            return self.scalar_multiply(other)
        elif isinstance(other, Point):
            result_x = self.x * other.x - self.y * other.y
            result_y = self.x * other.y + self.y * other.x
            return Point(result_x, result_y)
        else:
            raise TypeError("Unsupported operand type for *")
    def abs(self):
        return math.sqrt(self.x*self.x+self.y*self.y)
    def __truediv__ (self, other):
        return Point(self.x/other,self.y/other)
        
def rotate_around(poly,theta,origin):
    poly1=[]
    for e in poly:
        e1=(e-origin).rotate(theta)+origin
        poly1.append(e1)
    return poly1
def orientation(a, b, c):
    v = a.x*(b.y-c.y)+b.x*(c.y-a.y)+c.x*(a.y-b.y)
    if(v==0):return 0
    if (v < 0): return -1; #clockwise
    if (v > 0): return +1; # counter-clockwise

def cw(a, b, c, include_collinear):
    o = orientation(a, b, c)
    return o < 0 or (include_collinear and o == 0)

def collinear( a, b, c):  return (orientation(a, b, c) == 0)

def convex_hull(a, include_collinear = False):
    def custom_compare(a, b):
        if(a.y==b.y): 
            return a.x-a.y
        return a.y-b.y
    
    p0=min(a,key=cmp_to_key(custom_compare))
    def fitness(a,b):
        o = orientation(p0, a, b)
        if(o<0): return -1
        if(o>0): return 1
        if (o == 0):
            return (p0.x-a.x)*(p0.x-a.x) + (p0.y-a.y)*(p0.y-a.y) - (p0.x-b.x)*(p0.x-b.x) + (p0.y-b.y)*(p0.y-b.y)
    a=sorted(a, key=cmp_to_key(fitness))
    st=[]
    for i in range(0, len(a)):
        while (len(st)> 1 and cw(st[len(st)-2], st[len(st)-1], a[i], include_collinear)==0):
            st.pop()
        st.append(a[i])
    a = st
    return a

def rotate( poly, theta):
  poly1=[]
  for e in poly:
    e1=e.rotate(theta)
    poly1.append(e1)
  return poly1

def get_res_single_path(source, dest, poly, speed, rain, intense ):
  angle =(dest-source)/(dest-source).abs()*speed- rain
  rain_rel_velocity=(angle).abs()
  angle=(angle).conj()/(angle).abs()
  epsilon=1e-12
  mn=1/epsilon
  mx=-1/epsilon
  for e in poly:
    e1=e*angle
    mn=min(mn,e1.y)
    mx=max(mx,e1.y)
  proj=mx-mn
  time=(dest-source).abs()/speed
  ans=intense*proj*time*rain_rel_velocity
  return ans
def get_res_all_path(path, poly, speed, rain , intense):
  ans=0
  for i in range(1,len(path)):
    ans=ans+get_res_single_path(path[i-1],path[i],poly, speed, rain, intense)
  return ans
def solve(path, poly, rain , intense, speed, theta):
    poly1=rotate(poly, theta)
    return get_res_all_path(path, poly1, speed, rain, intense)

def objective(params, path, poly, rain, intense):
    speed, theta = params
    return solve(path, poly, rain, intense, speed, theta)  # Negate to minimize

initial_guess = [1.0, 90]  # Initial guess for speed and theta
bounds = [(0.001, math.inf), (0.0, 360)]  # Lower bounds for speed and theta

def solution(arr1, arr2, vx, vy, intense):
    global initial_guess, bounds
    origin_poly = [Point(point[0], point[1]) for point in arr1]
    path = [Point(point[0], point[1]) for point in arr2]
    rain = Point(vx, vy)
    poly = convex_hull(origin_poly)
    result = minimize(objective, initial_guess, args=(path, poly, rain, intense), method='Nelder-Mead', bounds=bounds)
    for theta in range(1, 360, 10):
        initial_guess[1]=theta
        res = minimize(objective, initial_guess, args=(path, poly, rain, intense), method='Nelder-Mead', bounds=bounds)
        if(res.fun<result.fun):result=res
    optimal_speed, optimal_theta = result.x
    optimal_result = result.fun  # Negate back to get the actual result
    sumx=0
    sumy=0
    for e in origin_poly:
        sumx=sumx+e.x
        sumy=sumy+e.y
    sumx=sumx/len(origin_poly)
    sumy=sumy/len(origin_poly)

    poly_ans=rotate_around(origin_poly,theta,Point(sumx,sumy))
    return [round(optimal_result, 3), round(optimal_speed, 3), round(optimal_theta, 3), [[round(e.x, 3), round(e.y, 3)] for e in poly_ans]]

if __name__ == "__main__":
    # Define constant parameters
    n = int(input())

    # Initialize a list to store the test cases
    origin_poly=[]

    # Read input for each test case
    for _ in range(n):
        a, b = map(float, input().split()) 
        origin_poly.append(Point(a, b))  
    p=int(input())
    path=[]
    for _ in range(p):
        a, b = map(float, input().split()) 
        path.append(Point(a, b))  
    a, b = map(float, input().split()) 
    rain=Point(a,b)
    intense=float(input())
    # path = pa  # Replace with your path data
    poly = origin_poly # Replace with your poly data
    # for e in poly:
    #     print(e.x,e.y)
    # rain = ...    # Replace with your rain value
    # intense = ... # Replace with your intense value

    initial_guess = [1.0, 90]  # Initial guess for speed and theta
    bounds = [(0.001, math.inf), (0.0, 360)]  # Lower bounds for speed and theta
    # print(objective((97489595,90),path,poly,rain, intense))
    # print(objective((97489595,0),path,poly,rain, intense))

    result = minimize(objective, initial_guess, args=(path, poly, rain, intense), method='Nelder-Mead', bounds=bounds)
    for theta in range(1, 360, 10):
        initial_guess[1]=theta
        res = minimize(objective, initial_guess, args=(path, poly, rain, intense), method='Nelder-Mead', bounds=bounds)
        if(res.fun<result.fun):result=res
    optimal_speed, optimal_theta = result.x
    optimal_result = result.fun  # Negate back to get the actual result
    print(optimal_result)
    print(optimal_speed)
    print(optimal_theta)
    sumx=0
    sumy=0
    for e in origin_poly:
        sumx=sumx+e.x
        sumy=sumy+e.y
    sumx=sumx/len(origin_poly)
    sumy=sumy/len(origin_poly)

    poly_ans=rotate_around(origin_poly,optimal_theta,Point(sumx,sumy))
    for e in poly_ans:
        print(e.x,e.y)