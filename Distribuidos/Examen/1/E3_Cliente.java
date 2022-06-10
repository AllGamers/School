import java.net.Socket;
import java.io.*;
import java.nio.ByteBuffer;
import java.lang.Thread;

class E3_Cliente{
	public static void main(String[] args) throws Exception{
		Socket conexion = null;
		for(;;){
			try{
				conexion=new Socket("sisdis.sytes.net",20020);
				break;
			}catch(Exception e){
				Thread.sleep(100);
			}
		}
		DataOutputStream salida = new DataOutputStream(conexion.getOutputStream());
		DataInputStream entrada = new DataInputStream(conexion.getInputStream());
		salida.writeDouble(92.0);
		salida.writeDouble(20.0);
		salida.writeDouble(52.0);
		salida.writeInt(29);
		double buffer = entrada.readDouble();
		System.out.println("Salida: " + buffer);
		salida.close();
		entrada.close();
		conexion.close();
	}
}