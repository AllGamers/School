import java.net.Socket;
import java.io.*;
import javax.net.ssl.SSLSocketFactory;
import java.io.FileInputStream;

class ClienteSSLMultiThreading{
	static byte[] leeArchivo(String archivo) throws Exception{
		FileInputStream f = new FileInputStream(archivo);
		byte[] buffer;
		try{
			buffer = new byte[f.available()];
			f.read(buffer);
		}finally{
			f.close();
		}
		return buffer;
	}

	public static void main(String[] args) throws Exception{
		SSLSocketFactory cliente = (SSLSocketFactory) SSLSocketFactory.getDefault();
		Socket conexion = null;
		for(;;){
			try{
				conexion=new Socket("localhost",50000);
				break;
			}catch(Exception e){
				Thread.sleep(100);
			}
		}
		if (args.length!=1){
			System.err.println("Uso:");
			System.err.println("java ClienteSSLMultiThreading <fileToSend>");
			System.exit(0);
		}
		String nameFile = args[0];
		DataOutputStream salida = new DataOutputStream(conexion.getOutputStream());
		DataInputStream entrada = new DataInputStream(conexion.getInputStream());
		while(conexion.isConnected()){
			salida.writeUTF(nameFile);
			byte[] buffer = leeArchivo(nameFile);
			salida.writeInt(buffer.length);
			salida.write(buffer);
		}
		Thread.sleep(10000);
		salida.close();
		entrada.close();
		conexion.close();
	}
}