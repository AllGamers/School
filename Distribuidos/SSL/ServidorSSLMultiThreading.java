import java.net.*;
import java.io.*;
import java.lang.*;
import javax.net.ssl.SSLServerSocketFactory;

class ServidorSSLMultiThreading{

	static void read(DataInputStream f, byte[] b,int posicion, int longitud) throws Exception{
		while(longitud>0){
			int n = f.read(b,posicion,longitud);
			posicion += n;
			longitud -= n;
		}
	}

	static void escribeArchivo(String archivo, byte[] buffer) throws Exception{
		FileOutputStream f = new FileOutputStream(archivo);
		try{
			f.write(buffer);
		}finally{
			f.close();
		}
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
				
				while(conexion.isConnected()){
					String nameFile = entrada.readUTF();
					int longFile = entrada.readInt();
					byte [] buffer = new byte[longFile];
					read(entrada,buffer,0,longFile);
					escribeArchivo(nameFile+"_Servidor",buffer);
				}
				Thread.sleep(10000);
				salida.close();
				entrada.close();
				conexion.close();
			}catch (Exception e){
				System.out.println("Error: "+e.getMessage());
			}
		}
	}

	public static void main(String[] args) throws Exception{
		SSLServerSocketFactory socket_factory = (SSLServerSocketFactory) SSLServerSocketFactory.getDefault();
		ServerSocket socket_servidor = socket_factory.createServerSocket(50000);
		for(;;){
			Socket conexion = socket_servidor.accept();
			Worker w = new Worker(conexion);
			w.start();
		}
	}
}