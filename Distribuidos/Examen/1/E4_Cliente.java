import java.net.Socket;
import java.io.*;
import java.nio.ByteBuffer;
import java.lang.Thread;

class E4_Cliente{
	public static void main(String[] args) throws Exception{
		Socket conexion = null;
		for(;;){
			try{
				conexion=new Socket("sisdis.sytes.net",50000);
				break;
			}catch(Exception e){
				Thread.sleep(100);
			}
		}
		DataOutputStream salida = new DataOutputStream(conexion.getOutputStream());
		DataInputStream entrada = new DataInputStream(conexion.getInputStream());
		
		Long T2 = entrada.readLong();
		Long T3 = entrada.readLong();

		Long T1 = new Long (1632744934);
		Long T4 = T3+3;

		Long resultado = ((T4-T1)-(T3-T2))/2;
		System.out.println(T3+resultado);

		salida.close();
		entrada.close();
		conexion.close();
	}
}