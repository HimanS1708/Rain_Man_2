import math
from scipy.optimize import minimize
from functools import cmp_to_key
import math

class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def conj(self):
        return Point3D(self.x, self.y, -self.z)

    def dot(self, other):
        """Calculate the dot product of two 3D points."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        """Calculate the cross product of two 3D points."""
        result_x = self.y * other.z - self.z * other.y
        result_y = self.z * other.x - self.x * other.z
        result_z = self.x * other.y - self.y * other.x
        return Point3D(result_x, result_y, result_z)

    def scalar_multiply(self, scalar):
        """Multiply the 3D point by a scalar."""
        return Point3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def rotate(self, angle_degrees, axis):
        """Rotate the 3D point by a given angle in degrees around the specified axis (x, y, or z)."""
        angle_radians = (angle_degrees)
        if axis == 'x':
            new_x = self.x
            new_y = self.y * math.cos(angle_radians) - self.z * math.sin(angle_radians)
            new_z = self.y * math.sin(angle_radians) + self.z * math.cos(angle_radians)
        elif axis == 'y':
            new_x = self.x * math.cos(angle_radians) + self.z * math.sin(angle_radians)
            new_y = self.y
            new_z = -self.x * math.sin(angle_radians) + self.z * math.cos(angle_radians)
        elif axis == 'z':
            new_x = self.x * math.cos(angle_radians) - self.y * math.sin(angle_radians)
            new_y = self.x * math.sin(angle_radians) + self.y * math.cos(angle_radians)
            new_z = self.z
        else:
            raise ValueError("Invalid axis. Use 'x', 'y', or 'z'.")
        return Point3D(new_x, new_y, new_z)

    def __add__(self, other):
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __neg__(self):
        return Point3D(-self.x, -self.y, -self.z)

    def __sub__(self, other):
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        """Support * operator for both scalar and point * point multiplication."""
        if isinstance(other, (int, float)):
            return self.scalar_multiply(other)
        elif isinstance(other, Point3D):
            result_x = self.x * other.x - self.y * other.y - self.z * other.z
            result_y = self.x * other.y + self.y * other.x
            result_z = self.x * other.z + self.z * other.x
            return Point3D(result_x, result_y, result_z)
        else:
            raise TypeError("Unsupported operand type for *")

    def abs(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def __truediv__(self, other):
        return Point3D(self.x / other, self.y / other, self.z / other)

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
        
def rotate_around3D(poly,theta,axis,origin):
    poly1=[]
    for e in poly:
        e1=(e-origin).rotate(theta,axis)+origin
        poly1.append(e1)
    return poly1
def orientation(a, b, c):
    v = a.x*(b.y-c.y)+b.x*(c.y-a.y)+c.x*(a.y-b.y)
    if(v==0):return 0
    if (v < 0): return -1; #clockwise
    if (v > 0): return +1; # counter-clockwise

def cw(a, b, c, include_collinear):
    o = orientation(a, b, c)

    return o < -1e-12 or (include_collinear and o == 0)

def collinear( a, b, c):  return (orientation(a, b, c) == 0)

def convex_hull(a, include_collinear = False):
    def custom_compare(a, b):
        if(a.y==b.y): 
            return a.x-a.y
        return a.y-b.y
    
    p0=min(a,key=cmp_to_key(custom_compare))
    def fitness(a,b):
        o = orientation(p0, a, b)
        if(o<-1e-12): return -1
        if(o>1e-12): return 1
        else:
            return (p0.x-a.x)*(p0.x-a.x) + (p0.y-a.y)*(p0.y-a.y) - (p0.x-b.x)*(p0.x-b.x) - (p0.y-b.y)*(p0.y-b.y)
    a=sorted(a, key=cmp_to_key(fitness))
    st=[]
    for i in range(0, len(a)):
        while (len(st)> 1 and cw(st[len(st)-2], st[len(st)-1], a[i], include_collinear)==0):
            st.pop()
        st.append(a[i])
    a = st
    return a

def rotate3D( poly, theta,axis):
  poly1=[]
  for e in poly:
    e1=e.rotate(theta,axis)
    poly1.append(e1)
  return poly1
def area(poly1):
    poly=convex_hull(poly1)
    poly.append(poly[0])
    ans=0

    for i in range(0, len(poly)-1):
        ans=ans+poly[i+1].cross(poly[i])
    ans=abs(ans)
    return ans
def get_angle(y, x):
    if(x==0):
        if(y>0):return 90
        else: return -90
    if(x<0):
        return math.atan(y/x)+math.pi
    else:
        return math.atan(y/x)
    # else: return math.atan(y/x)*180/math.pi
def get_res_single_path3D(source, dest, poly, speed, rain, intense ):
  angle =(dest-source)/(dest-source).abs()*speed- rain
  rain_rel_velocity=(angle).abs()
  angle=(angle)/(angle).abs()
  axis='z'
  theta=get_angle(angle.y,angle.x)
  poly=rotate3D(poly,theta,axis)
#   print(angle.x,angle.y,angle.z)
  angle=angle.rotate(theta,axis)
#   print(angle.x,angle.y,angle.z)
#   print(theta)
  axis='y'
  theta=get_angle(angle.z,angle.x)
  poly=rotate3D(poly, theta, axis)
  angle=angle.rotate(theta,axis)
#   print(angle.x,angle.y,angle.z)
  poly_proj=[]
  for e in poly:
    poly_proj.append(Point(e.y, e.z))
  proj=area(poly_proj)
#   if proj==0:
#       for e in poly_proj:
#           print(e.x,e.y)
  time=(dest-source).abs()/speed
  ans=intense*proj*time*rain_rel_velocity
  return ans
def get_res_all_path(path, poly, speed, rain , intense):
  ans=0
  for i in range(1,len(path)):
    ans=ans+get_res_single_path3D(path[i-1],path[i],poly, speed, rain, intense)
  return ans
def solve(path, poly, rain , intense, speed, theta,alpha):
    poly1=rotate3D(poly, theta,'x')
    poly1=rotate3D(poly1,alpha,'y')
    return get_res_all_path(path, poly1, speed, rain, intense)

def objective(params, path, poly, rain, intense):
    speed, theta, alpha = params
    return solve(path, poly, rain, intense, speed, theta,alpha)  # Negate to minimize

initial_guess = [1.0, 90,90]  # Initial guess for speed and theta
bounds = [(0.001, math.inf), (0.0, 360),(0.0,360)]  # Lower bounds for speed and theta

def solution(arr1, arr2, rx, ry, rz, intense):
    origin_poly = [Point3D(p.x, p.y, p.z) for p in arr1]
    path = [Point3D(p.x, p.y, p.z) for p in arr2]
    rain = Point3D(rx, ry, rz)
    result = minimize(objective, initial_guess, args=(path, origin_poly, rain, intense), method='Nelder-Mead', bounds=bounds)
    for alpha in range(1, 360,39):
        initial_guess[2]=alpha
        for theta in range(1, 360, 39):
            initial_guess[1]=theta
            res = minimize(objective, initial_guess, args=(path, origin_poly, rain, intense), method='L-BFGS-B', bounds=bounds)
            if(res.fun<result.fun):
                result=res
    optimal_speed, optimal_theta, optimal_alpha = result.x
    optimal_result = result.fun  # Negate back to get the actual result
    sumx=0
    sumy=0
    sumz=0
    for e in origin_poly:
        sumx=sumx+e.x
        sumy=sumy+e.y
        sumz=sumz+e.z
    sumx=sumx/len(origin_poly)
    sumy=sumy/len(origin_poly)
    sumz=sumz/len(origin_poly)

    poly_ans=rotate_around3D(origin_poly,optimal_theta,'x',Point3D(sumx,sumy,sumz))
    poly_ans=rotate_around3D(poly_ans,optimal_alpha,'y',Point3D(sumx,sumy,sumz))
    return [round(optimal_result, 4), round(optimal_speed, 4), round(optimal_theta, 4), round(optimal_alpha, 4), [[round(e.x, 4), round(e.y, 4), round(e.z, 4)] for e in poly_ans]]

if __name__ == "__main__":
    # Define constant parameters
    n = int(input())

    # Initialize a list to store the test cases
    origin_poly=[]

    # Read input for each test case
    for _ in range(n):
        a, b,c = map(float, input().split()) 
        origin_poly.append(Point3D(a, b,c))  
    p=int(input())
    path=[]
    for _ in range(p):
        a, b,c = map(float, input().split()) 
        path.append(Point3D(a, b,c))  
    a, b,c = map(float, input().split()) 
    rain=Point3D(a,b,c)
    intense=float(input())

    initial_guess = [1.0, 90,90]  # Initial guess for speed and theta
    bounds = [(0.001, math.inf), (0.0, 360),(0.0,360)]  # Lower bounds for speed and theta
    # print(objective((97489595,90),path,poly,rain, intense))
    # print(objective((97489595,0),path,poly,rain, intense))

    result = minimize(objective, initial_guess, args=(path, origin_poly, rain, intense), method='Nelder-Mead', bounds=bounds)
    for alpha in range(1, 360,39):
        initial_guess[2]=alpha
        for theta in range(1, 360, 39):
            initial_guess[1]=theta
            res = minimize(objective, initial_guess, args=(path, origin_poly, rain, intense), method='L-BFGS-B', bounds=bounds)
            if(res.fun<result.fun):
                result=res

    optimal_speed, optimal_theta, optimal_alpha = result.x
    optimal_result = result.fun  # Negate back to get the actual result
    print(round(optimal_result,3))
    print(optimal_speed)
    print(optimal_theta)
    print(optimal_alpha)
    sumx=0
    sumy=0
    sumz=0
    for e in origin_poly:
        sumx=sumx+e.x
        sumy=sumy+e.y
        sumz=sumz+e.z
    sumx=sumx/len(origin_poly)
    sumy=sumy/len(origin_poly)
    sumz=sumz/len(origin_poly)

    poly_ans=rotate_around3D(origin_poly,optimal_theta,'x',Point3D(sumx,sumy,sumz))
    poly_ans=rotate_around3D(poly_ans,optimal_alpha,'y',Point3D(sumx,sumy,sumz))
    for e in poly_ans:
        print(round(e.x,4),round(e.y,4),round(e.z,4))