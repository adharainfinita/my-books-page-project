import express from "express"
import cors from "cors"
import morgan from "morgan"

const server = express();

//? Middlewares
server.use(express.json());
server.use(morgan('dev'));
server.use(cors());
//server.use(log);

//? Routes





export default server;