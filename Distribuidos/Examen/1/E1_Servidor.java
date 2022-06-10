import java.net.*;
import java.io.*;
import java.nio.ByteBuffer;
import java.lang.*;

class E1_Servidor{
	public static void main(String[] args) throws Exception{
		Double total = 0.0;
		ServerSocket conexion = new ServerSocket(50000);
		Socket cl = conexion.accept(); 
		DataOutputStream salida = new DataOutputStream(cl.getOutputStream());
		DataInputStream entrada = new DataInputStream(cl.getInputStream());
		byte[] a = new byte[1000*8];
		read(entrada,a,0,1000*8);
		ByteBuffer b = ByteBuffer.wrap(a);
		for (int i=0;i<1000;i++){total += b.getInt();}
		System.out.println("Total :"+total);
		salida.close();
		entrada.close();
		conexion.close();
	}

	static void read(DataInputStream f, byte[] b,int posicion, int longitud) throws Exception{
		while(longitud>0){
			int n = f.read(b,posicion,longitud);
			posicion += n;
			longitud -= n;
		}
	}
}