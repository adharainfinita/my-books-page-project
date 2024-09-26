import server from "./app";

process.loadEnvFile('.env')

const PORT = process.env.PORT || 3000;

try {
  server.listen(PORT, ()=> {
      console.log(`Server raised with exit in port: ${PORT}`)
  })
} catch (error) {
  const typedError = error as Error;  
  console.error('Failed to start server: ', typedError.message)
}

//? Manejador global para promesas no manejadas
process.on('uncaughtException', (reason:any, promise:any)=> {
  console.error('Unhandled Rejection at: ', promise, 'reason: ', reason);
  process.exit(1) // Termina el proceso si hay un error crítico
});


