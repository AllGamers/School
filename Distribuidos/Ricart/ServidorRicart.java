import java.net.*;
import java.lang.Thread;
import java.io.*;

enum Estado{
	Normal,EsperandoRecurso,AdquirioRecurso;
}

class ServidorRicart{
	static String[] hosts;
	static int [] puertos;
	static int num_nodos;
	static int nodo;

	static long reloj_logico;
	static Object lock = new Object();

	static LinkedList<Integer> cola = new LinkedList<Integer>();

	static int num_ok_recibidos;
	static long tiempo_logico_enviado;

	static Estado estado = Estado.Normal;

	static void envia_mensaje(long tiempo_logico, String host, int puerto) throws Exception{
		Socket conexion = null;
		for(;;){
			try{
				conexion = new Socket(host,puerto);
				break;
			}catch(Exception e){
				Thread.sleep(100);
			}
		}
		DataOutputStream salida = new DataOutputStream(conexion.getOutputStream());
		salida.writeInt(nodo);
		salida.writeLong(tiempo_logico);
		salida.close();
		conexion.close();
	}

	static class Reloj extends Thread{
		public void run(){
			for(;;){
				try{
					synchronized(lock){
						System.out.println(reloj_logico);
						if(nodo==0){
							reloj_logico+=4;
						}
						if(nodo==1){
							reloj_logico+=5;	
						}
						if(nodo==2){
							reloj_logico+=6;
						}
					}
					Thread.sleep(1000);
				}catch(Exception e){
					System.out.println("Error Reloj: "+e.getMessage());
				}
			}
		}
	}

	static class Worker extends Thread{
		Socket conexion;
		Worker(Socket conexion){
			this.conexion=conexion;
		}
		public void run(){
			try{
				DataInputStream entrada = new DataInputStream(conexion.getInputStream());
				System.out.println("Inicio el thread Worker");
				for(;;){
					int nodo_recibido;
					long tiempo_recibido;
					nodo_recibido = entrada.readInt();
					tiempo_recibido = entrada.readLong();
					if(tiempo_recibido>0){
						synchronized(lock){
							if(tiempo_recibido>reloj_logico){
								reloj_logico=tiempo_recibido+1;
							}
						}
					}
				}
			}catch (Exception e){
				//System.out.println("Error Worker: "+e.getMessage());
			}
		}
	}

	static class Servidor extends Thread{
		public void run(){
			try{
				ServerSocket servidor = new ServerSocket(puertos[nodo]);
				for(;;){
					Socket conexion = servidor.accept();
					Worker w = new Worker(conexion);
					w.start();
				}
			}catch (Exception e){
				System.out.println("Error Servidor: "+e.getMessage());
			}
		}
	}

	static void bloquea() throws Exception{
		estado = Estado.EsperandoRecurso;
		num_ok_recibidos = 0;
		tiempo_logico_enviado=reloj_logico;
		for(int i=0; i<num_nodos; i++){
			if(i!=nodo){
				envia_peticion(1,nodo,tiempo_logico_enviado,hosts[i],puertos[i]);
			}
		}
	}

	static void desbloquea() throws Exception{
		estado = Estado.Normal;
		while(cola.size()>0){
			int nodo = cola.removeFirst();
			envia_ok(reloj_logico,hosts[nodo],puertos[nodo]);
		}
	}


	public static void main(String[] args) throws Exception{
		if(args.length < 2){
			System.err.println("Uso:");
			System.err.println("java ServidorRicart <nodo> <host>:<puerto> ...");	
		}
		nodo = Integer.valueOf(args[0]);
		num_nodos = args.length - 1;

		hosts = new String[num_nodos];
		puertos = new int[num_nodos];

		for (int i=0; i<num_nodos; i++){
			hosts[i] = args[i+1].split(":")[0];
			puertos[i] = Integer.valueOf(args[i+1].split(":")[1]);
		}

		Servidor s = new Servidor();
		s.start();

		for (int i=0; i<num_nodos; i++){
			envia_mensaje(0, hosts[i], puertos[i]);
		}

		Reloj r = new Reloj();
		r.start();

		Thread.sleep(1000);
		bloquea();
		while (estado!=Estado.AdquirioRecurso) Thread.sleep(100);
		desbloquea();
		Thread.sleep(3000);
		s.join();
	}
}