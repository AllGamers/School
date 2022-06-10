import java.net.*;
import java.io.*;
import java.nio.ByteBuffer;
import java.lang.*;
import javax.net.ssl.SSLServerSocketFactory;

class ServidorSSL{
	public static void main(String[] args) throws Exception{
		SSLServerSocketFactory socket_factory = (SSLServerSocketFactory) SSLServerSocketFactory.getDefault();
		ServerSocket socket_servidor = socket_factory.createServerSocket(50000);
		Socket conexion = socket_servidor.accept();

		DataOutputStream salida = new DataOutputStream(conexion.getOutputStream());
		DataInputStream entrada = new DataInputStream(conexion.getInputStream());

		System.out.println(entrada.readDouble());

		salida.close();
		entrada.close();
		conexion.close();
	}
}

//java -Djavax.net.ssl.keyStore=keystore_servidor.jks -Djavax.net.ssl.keyStorePassword=1234567 ServidorSSL
//java -Djavax.net.ssl.trustStore=keystore_cliente.jks -Djavax.net.ssl.trustStorePassword=123456 ClienteSSL