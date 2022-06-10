import java.net.*;
import java.io.*;
import java.nio.ByteBuffer;
import java.lang.*;

class ServidorMultiThreading{

	static int coordinador_actual;

	static String envia_mensaje_eleccion(String host, int puerto){
		Socket conexion = null;
		try{
			DataOutputStream salida = new DataOutputStream(conexion.getOutputStream());
			DataInputStream entrada = new DataInputStream(conexion.getInputStream());
			String mensaje;
			conexion = new Socket(host,puerto);
			salida.writeUTF("ELECCION");
			mensaje = entrada.readUTF();
			salida.close();
			entrada.close();
			conexion.close();
			return mensaje;
		}catch(Exception e){
			return "";
		}
		
	}

	static void envia_mensaje_coordinador(String host, int puerto){
		Socket conexion = null;
		try{
			DataOutputStream salida = new DataOutputStream(conexion.getOutputStream());
			DataInputStream entrada = new DataInputStream(conexion.getInputStream());
			conexion = new Socket(host,puerto);
			salida.writeUTF("COORDINADOR");
			salida.writeInt(coordinador_actual);
			salida.close();
			entrada.close();
			conexion.close();
		}catch(Exception e){
			
		}
		
	}

	static void eleccion(int nodo){
		
	}

	static class Worker extends Thread{
		Socket conexion;
		Worker(Socket conexion){
			this.conexion=conexion;
		}
		public void run(){
			try{
				DataOutputStream salida = new DataOutputStream(conexion.getOutputStream());
				DataInputStream entrada = new DataInputStream(conexion.getInputStream());
				
				String mensaje;

				mensaje = readUTF();

				if(mensaje.equals("ELECCION")){
					salida.writeUTF("OK");
					eleccion(nodo);
				}

				if(mensaje.equals("COORDINADOR")){
					coordinador_actual = salida.readInt();
					eleccion(nodo);
				}

				salida.close();
				entrada.close();
				conexion.close();
			}catch (Exception e){
				System.out.println("Error run: "+e.getMessage());
			}
		}
	}
	public static void main(String[] args) throws Exception{
		ServerSocket servidor = new ServerSocket(50000);
		for(;;){
			Socket conexion = servidor.accept();
			Worker w = new Worker(conexion);
			w.start();
		}
	}
}