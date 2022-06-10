import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;


public class EleccionAnillo {

    private static long token;
    private static double[] M = new double[5];
    private static boolean[] B = new boolean[5];

    private static boolean status_bloqueo = false;
    private static boolean tengo_token = false;
    /*lock - unlock*/
    private static Object bloqueo = new Object();
    private static Object tengo_token_block = new Object();

    private static String[] hosts;
    private static Integer[] ports;
    private static int nodo;
    private static int num_nodos;

    static class Worker extends Thread {
        Socket Conexion;

        Worker(Socket Conexion) {
            this.Conexion = Conexion;
        }

        public void run() {
            try {
                // Buffers
                DataInputStream entrada = new DataInputStream(Conexion.getInputStream());
                
                token = entrada.readLong();
                synchronized (tengo_token_block) {
                    tengo_token = true;
                }
                System.out.println("t:" + token);
                token++;
                while (true) {
                    synchronized (bloqueo) {
                        if (status_bloqueo == false) {
                            break;
                        }
                    }
                }
                envia_token(token, hosts[(nodo + 1) % num_nodos], ports[(nodo + 1) % num_nodos]);
                // close buffer and conection
                entrada.close();
                Conexion.close();
            } catch (IOException ex) {

            } catch (Exception e) {

            }
        }
    }

    static class Servidor extends Thread {
        public void run() {
            System.out.println("Servidor iniciado");
            ServerSocket servidor;
            try {
                servidor = new ServerSocket(ports[nodo]);
                for (;;) {
                    Socket cliente = servidor.accept();
                    Worker x = new Worker(cliente);
                    x.start();
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        if (args.length < 2) {
            System.err.print("Uso:");
            System.err.print("java EleccionAnillo <nodo> <ip1:puerto1> <ip2:puerto2>  ... <ipN:puertoN>");
            System.exit(0);
        }
        num_nodos = (args.length - 1);
        nodo = Integer.parseInt(args[0]);
        System.out.println(nodo);
        hosts = new String[args.length];
        ports = new Integer[args.length];
        for (int i = 1; i < args.length; i++) {
            hosts[i - 1] = args[i].split(":")[0];
            ports[i - 1] = Integer.parseInt(args[i].split(":")[1]);
        }
        Servidor s = new Servidor();
        s.start();

        if (revisaConexiones()) {
            if (nodo == 0) {
                synchronized (tengo_token_block) {
                    tengo_token = true;
                }
                envia_token(1, hosts[1], ports[1]);
            }
            Thread.sleep(3000);
            if (nodo == 0) {
                lock();
                Thread.sleep(3000);
                unlock();
            }
            if (nodo == 1) {
                lock();
                Thread.sleep(3000);
                unlock();
            }
            if (nodo == 2) {
                lock();
                Thread.sleep(3000);
                unlock();
            }
            if (nodo == 3) {
                lock();
                Thread.sleep(3000);
                unlock();
            }
        }
    }

    private static boolean revisaConexiones() {
        for (int i = 0; i < num_nodos; i++) {
            envia_mensaje_Barrera(hosts[i], ports[i]);
        }
        return true;
    }

    private static void envia_mensaje_Barrera(String host, Integer port) {
        Socket cliente = null;
        for (;;) {
            try {
                cliente = new Socket(host, port);
                System.out.println("Conecte con " + host +":"+ port);
                try {
                } catch (Exception e) {
                    System.out.println(e);
                } finally {
                    cliente.close();
                }
                break;
            } catch (IOException e1) {
            }
        }
    }

    private static double read(int n) throws Exception {
        return M[n];
    }

    private static void write(int n, double valor)throws Exception{
        M[n] = valor;
        B[n] = true;
    }

    private static void unlock() {
        synchronized (bloqueo) {
            System.out.println("Desbloqueo el nodo:" + nodo);
            status_bloqueo = false;
        }
    }

    private static void lock() {
        for (int i=0;i<B.length();i++){
            B[i] = false;
        }
        // Espera a tener el token
        while (true) {
            synchronized (tengo_token_block) {
                if (tengo_token) {
                    break;
                }
            }
        }
        // bloqueo de nodo
        synchronized (bloqueo) {
            System.out.println("Bloqueo el nodo:" + nodo);
            status_bloqueo = true;
        }
    }

    private static void envia_token(long value, String host, Integer port) {
        Socket cliente = null;
        for (;;) {
            try {
                cliente = new Socket(host, port);
                try {
                    DataOutputStream salida = new DataOutputStream(cliente.getOutputStream());
                    salida.writeLong(value);
                    synchronized (tengo_token_block) {
                        tengo_token = false;
                    }
                } catch (Exception e) {
                    System.out.println(e);
                } finally {
                    cliente.close();
                    break;
                }
            } catch (IOException e1) {
            }
        }
    }

    

}
