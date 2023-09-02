import {useState, useEffect, useRef} from "react";
import {Button, TextField} from "@mui/material";
import './App.css';

function random(min, max) {
    return Math.random() * (max - min) + min;
}

function App() {
	const canvasRef = useRef(null)
	const [objPts, setObjPts] = useState([[0, 100], [100, 0], [3, 3]]);
	const [pathPts, setPathPts] = useState([[0, 0], [100, 100], [200, 200]]);
	const [rainParam, setRainParam] = useState({velX: 0, velY:0, density: 0});
	const[idealV, setIdealV] = useState("none");
	
	useEffect(() => {
		const canvas = canvasRef.current;
		const ctx = canvasRef.current.getContext("2d");
		const {velX, velY} = rainParam;
		class Raindrop {
			constructor() {
			  this.x = random(0, canvas.width);
			  this.y = random(0, canvas.height);
			  this.speedx = velX;
			  this.speedy = velY;
			  this.length = random(0, 1);
			  this.thickness = random(5, 10);
			}

			fall() {
			  this.y += this.speedy;
			  this.x += this.speedx;
			  if (this.y > canvas.height || this.x> canvas.width || this.x<0) {
				if(random(0,1)>=(canvas.width/(canvas.width+canvas.height))){
				this.x=0;    
				this.y = random(0, canvas.height);
				}
				else{
				this.x = random(0, canvas.width);
				this.y=0;
				}
			  }
			}
			
			draw() {
				// ctx.clearRect(0, 0, canvas.width, canvas.height)
				const costheta = velY/Math.sqrt(Math.pow(velX,2)+Math.pow(velY,2))
				const sintheta = velX/Math.sqrt(Math.pow(velX,2)+Math.pow(velY,2))
			  ctx.beginPath();
			  ctx.strokeStyle = 'blue';
			  ctx.lineWidth = this.thickness;
			  ctx.moveTo(this.x, this.y);
			  ctx.lineTo(this.x - (this.length*costheta), this.y + (this.length*sintheta));
			  ctx.stroke();
			}
		}
		
		const raindrops = [];
		for (let i = 0; i < rainParam.density; i++) {
			raindrops.push(new Raindrop());
		}
// 		let path = [[0, 0], [100, 100], [100, 200]];
		let path = pathPts;
		let shift = [];
		let segIdx = 0;
		let animId;
		function draw() { 
			ctx.clearRect(0, 0, canvas.width, canvas.height);
			for (const drop of raindrops) {
				drop.fall();
				drop.draw();
			}
			//draw object translated by shift
			ctx.strokeStyle = 'black';
			ctx.lineWidth = 0.5;
			let interpPts = objPts.map(pt => [Number(pt[0]) + Number(shift[0]), Number(pt[1]) + Number(shift[1])])
			ctx.beginPath();	
			ctx.moveTo(interpPts[0][0],interpPts[0][1]);
			interpPts.forEach((pt) => {
				ctx.lineTo(pt[0], pt[1])
			});
			ctx.lineTo(interpPts[0][0],interpPts[0][1]);
			ctx.stroke()
			segIdx += 0.005*(idealV === 'none' ? 1 : idealV);
			if (segIdx > path.length - 1) {
				console.log(segIdx);
				segIdx = 0;
			}
			let segIdxFrac = segIdx- Math.floor(segIdx)
			
// 			shift[0] = path[Math.floor(segIdx)][0]*(Math.ceil(segIdx) - segIdx) + path[Math.ceil(segIdx)][0]*(segIdx - Math.floor(segIdx));
// 			shift[1] = path[Math.floor(segIdx)][1]*(Math.ceil(segIdx) - segIdx) + path[Math.floor(segIdx)][1]*(segIdx - Math.floor(segIdx));
			shift[0] = (1 - segIdxFrac)*path[Math.floor(segIdx)][0] + (segIdxFrac)*(path[Math.ceil(segIdx)][0]);
			shift[1] = (1 - segIdxFrac)*path[Math.floor(segIdx)][1] + (segIdxFrac)*(path[Math.ceil(segIdx)][1]);
			
			
			
			animId = requestAnimationFrame(draw);
		}
		draw();
		return () => {
			cancelAnimationFrame(animId)
		}
	});
	
	
  return (
	<div>
		<canvas 
			ref={canvasRef} 
			width={0.8*window.innerWidth} 
			height={0.8*window.innerHeight} 
			style={{border:"solid 1px #000"}}
		></canvas>
		<div className="inputs" style={{display:"flex", width:"100%"}}>
		<div className="obj-input">
			<h3>Object vertices</h3>
			<ol>
				{
				objPts.map((el, idx) => (
					<li key={`obj-pt${idx}`}>
					<TextField 
						key={`obj-x${idx}`}
						type="number"
						value={objPts[idx][0]}
						onChange={(event) => {
// 							let newPts = objPts;
// 							newPts[idx][0] = event.target.value;
							setObjPts([...objPts.slice(0,idx), [event.target.value, objPts[idx][1]], ...objPts.slice(idx+1)]);
						}}
					/>
					<TextField 
						key={`obj-y${idx}`}
						type="number"
						value={objPts[idx][1]}
						onChange={(event) => {
							setObjPts([...objPts.slice(0,idx), [objPts[idx][0], event.target.value], ...objPts.slice(idx+1)]);
						}}
					/>
					</li>
				))
				}
			</ol>
			<Button onClick={() => {
				setObjPts([...objPts, [0,0]]);
			}}>Add Point</Button>
			<Button onClick={() => {
				if (objPts.length > 2) setObjPts([...objPts.slice(0,objPts.length - 1)])
			}}>Delete Last Point</Button>
		</div>
		<div className="rain-input">
			<h3>Rain Parameters</h3>
			<h4>X velocity</h4>
			<TextField
				type="number"
				value={rainParam.velX}
				onChange={(e) => {
					setRainParam({...rainParam, velX: Number(e.target.value)})
				}}
			/>
			<h4>Y velocity</h4>
			<TextField
				type="number"
				value={rainParam.velY}
				onChange={(e) => {
					setRainParam({...rainParam, velY: Number(e.target.value)})
				}}
			/>
			<h4>Density</h4>
			<TextField
				type="number"
				value={rainParam.density}
				onChange={(e) => {
					setRainParam({...rainParam, density: Math.max(0, Number(e.target.value))})
				}}
			/>
			
		</div>
		<div className="path-input">
			<h3>Path vertices</h3>
			<ol>
				{
				pathPts.map((el, idx) => (
					<li key={`path-pt${idx}`}>
					<TextField 
						key={`path-x${idx}`}
						type="number"
						value={pathPts[idx][0]}
						onChange={(event) => {
							setPathPts([...pathPts.slice(0,idx), [event.target.value, pathPts[idx][1]], ...pathPts.slice(idx+1)]);
						}}
					/>
					<TextField 
						key={`path-y${idx}`}
						type="number"
						value={pathPts[idx][1]}
						onChange={(event) => {
							setPathPts([...pathPts.slice(0,idx), [pathPts[idx][0], event.target.value], ...pathPts.slice(idx+1)]);
						}}
					/>
					</li>
				))
				}
			</ol>
			<Button onClick={() => {
				setPathPts([...pathPts, [0,0]]);
			}}>Add Point</Button>
			<Button onClick={() => {
				if (pathPts.length > 2) setPathPts([...pathPts.slice(0,pathPts.length - 1)])
			}}>Delete Last Point</Button>
		</div>
		<Button onClick={() => {
			//return:
    		fetch("http://localhost:8000/", {
        		method: "POST",
        		body: JSON.stringify({
					"points":objPts,
					"path_points":pathPts,
					"v_x": rainParam.velX,
					"v_y": rainParam.velY,
					"v_z": 0,
					"intensity": rainParam.density
        		}),
        		headers: {
            		"Content-type": "application/json; charset=UTF-8"
        		}
    		})
    		.then(response => response.json())
    		.then(json => {
    			setObjPts(json[3]);
    			setIdealV(json[1]);
    		})
    		.catch(err => (console.log(err)));
		}}>Submit</Button>
		</div>
	</div>
  );
}

export default App;
