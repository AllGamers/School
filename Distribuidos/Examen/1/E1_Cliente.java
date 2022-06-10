import java.net.Socket;
import java.io.*;
import java.nio.ByteBuffer;
import java.lang.Thread;

class E1_Cliente{
	public static void main(String[] args) throws Exception{
		Socket conexion = null;
		for(;;){
			try{
				conexion=new Socket("localhost",50000);
				break;
			}catch(Exception e){
				Thread.sleep(100);
			}
		}
		DataOutputStream salida = new DataOutputStream(conexion.getOutputStream());
		DataInputStream entrada = new DataInputStream(conexion.getInputStream());
		ByteBuffer b = ByteBuffer.allocate(1000*8);
		for(int i=0;i<=1000;i++){
			if (i%2==0){

				b.putInt(i);
			}
		}
		byte[]a=b.array();
		salida.write(a);
		Thread.sleep(500);
		salida.close();
		entrada.close();
		conexion.close();
	}
}