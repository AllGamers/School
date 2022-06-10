import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.LinkedList;


public class ExclusionMutua {
    enum Estado {
        Normal, Esperando, Adquirido
    }

    private static String[] hosts;
    private static Integer[] ports;
    private static int nodo;
    private static int num_nodos;

    private static long reloj_logico = 0;
    private static Object o = new Object();

    static int num_ok_recibidos;
    private static long tiempo_logico_enviado;
    private static Estado estado = Estado.Normal;
    private static LinkedList<Integer> Cola = new LinkedList<>();

    static class Worker extends Thread {
        Socket Conexion;

        Worker(Socket Conexion) {
            this.Conexion = Conexion;
        }

        public void run() {
            try {
                // Buffers
                DataInputStream entrada = new DataInputStream(Conexion.getInputStream());
                // ** Cuerpo del programa ** //
                // System.out.println("Inicio el thread worker");
                String command = entrada.readUTF();
                if (command.equals("Request")) {
                    recibe_peticion(entrada);
                }
                if (command.equals("Ok")) {
                    recibe_ok(entrada);
                }
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

    static class Reloj extends Thread {
        public void run() {
            for (;;) {
                System.out.println("Rl:" + reloj_logico);
                if (nodo == 0) {
                    synchronized (o) {
                        reloj_logico += 4;
                    }
                } else if (nodo == 1) {
                    synchronized (o) {
                        reloj_logico += 5;
                    }
                } else if (nodo == 2) {
                    synchronized (o) {
                        reloj_logico += 6;
                    }
                }
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        if (args.length < 2) {
            System.err.print("Uso:");
            System.err.print("java ExclusionMutua <nodo> <ip1:puerto1> <ip2:puerto2>  ... <ipN:puertoN>");
            System.exit(0);
        }
        nodo = Integer.parseInt(args[0]);
        System.out.println(nodo);
        num_nodos = (args.length - 1);
        System.out.println(num_nodos);
        hosts = new String[args.length];
        ports = new Integer[args.length];
        for (int i = 1; i < args.length; i++) {
            hosts[i - 1] = args[i].split(":")[0];
            ports[i - 1] = Integer.parseInt(args[i].split(":")[1]);
        }

        Servidor s1 = new Servidor();
        s1.start();

        if (revisaConexiones()) {
            System.out.println("Barrera Superada");
            Reloj r1 = new Reloj();
            r1.start();

            Thread.sleep(1000);

            bloquea();

            while (estado != Estado.Adquirido) {
                Thread.sleep(100);
            }

            Thread.sleep(3000);

            desbloquea();

            try {
                s1.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    private static void desbloquea() {
        System.out.println(">>>>>>>Desbloqueear<<<<<<<");
        printCola();
        estado = Estado.Normal;
        for (int i = 0; i < Cola.size(); i++) {
            int nodo_tmp = Cola.get(i);
            synchronized (o) {
                System.out.println(" Intento Enviar ok a " + hosts[nodo_tmp] + ":" + ports[nodo_tmp]);
                envia_Ok(reloj_logico, hosts[nodo_tmp], ports[nodo_tmp]);
                System.out.println("Envie ok a " + hosts[nodo_tmp] + ":" + ports[nodo_tmp]);
            }
        }
        Cola.clear();
    }

    private static void bloquea() {
        estado = Estado.Esperando;
        num_ok_recibidos = 0;
        synchronized (o) {
            tiempo_logico_enviado = reloj_logico;
            System.out.println(">>>>>>>Bloquea<<<<<<< en " + tiempo_logico_enviado);
        }
        for (int i = 0; i < num_nodos; i++) {
            if (i != nodo) {
                envia_peticion(1, tiempo_logico_enviado, hosts[i], ports[i]);
            }
        }
    }

    static void envia_Barrera(String host, int port) {
        Socket cliente;
        for (;;) {
            try {
                cliente = new Socket(host, port);
                DataOutputStream salida = new DataOutputStream(cliente.getOutputStream());
                salida.writeUTF("Barrera");
                cliente.close();
                salida.close();
                break;
            } catch (Exception e) {
            }
        }
    }

    static void envia_Ok(long tiempo_logico, String host, int port) {
        Socket cliente;
        for (;;) {
            try {
                cliente = new Socket(host, port);
                DataOutputStream salida = new DataOutputStream(cliente.getOutputStream());
                salida.writeUTF("Ok");
                salida.writeLong(tiempo_logico);
                cliente.close();
                salida.close();
                break;
            } catch (Exception e) {
            }
        }
    }

    private static void recibe_ok(DataInputStream entrada) {
        try {
            num_ok_recibidos++;
            long tiempo_recibido;
            tiempo_recibido = entrada.readLong();
            System.out.println("~Ok~" + tiempo_recibido);
            lamport(tiempo_recibido);
            if (num_ok_recibidos == num_nodos - 1) {
                System.out.println("~~~~~~~Adquiri el recurso~~~~~~~");
                estado = Estado.Adquirido;
            }
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    static void envia_peticion(int id, long tiempo_logico_enviado, String host, int port) {
        Socket cliente;
        for (;;) {
            try {
                cliente = new Socket(host, port);
                DataOutputStream salida = new DataOutputStream(cliente.getOutputStream());
                salida.writeUTF("Request");
                salida.writeInt(id);
                salida.writeInt(nodo);
                salida.writeLong(tiempo_logico_enviado);
                System.out.println("Envie peticion a " + host + ":" + port);
                cliente.close();
                salida.close();
                break;
            } catch (Exception e) {
            }
        }
    }

    static void recibe_peticion(DataInputStream entrada) {
        int id_recibido;
        int nodo_recibido;
        long tiempo_recibido;// T1
        try {
            id_recibido = entrada.readInt();
            nodo_recibido = entrada.readInt();
            tiempo_recibido = entrada.readLong();
            System.out.println("----------\nID recurso:" + id_recibido);
            System.out.println("Tiempo recibido:" + tiempo_recibido);
            System.out.println("Reloj logico:" + reloj_logico);
            System.out.println("Estado:" + estado + "\n----------");
            lamport(tiempo_recibido);
            if (nodo_recibido == nodo) {
                synchronized (o) {
                    envia_Ok(reloj_logico, hosts[nodo_recibido], ports[nodo_recibido]);
                }
            } else if (estado == Estado.Adquirido) {
                Cola.add(nodo_recibido);
            } else if (estado == Estado.Normal) {
                synchronized (o) {
                    envia_Ok(reloj_logico, hosts[nodo_recibido], ports[nodo_recibido]);
                }
            } else if (estado == Estado.Esperando) {
                if (tiempo_recibido < tiempo_logico_enviado) {
                    synchronized (o) {
                        envia_Ok(reloj_logico, hosts[nodo_recibido], ports[nodo_recibido]);
                    }
                } else if (tiempo_logico_enviado < tiempo_recibido) {
                    Cola.add(nodo_recibido);
                } else if (tiempo_recibido == tiempo_logico_enviado) {
                    if (nodo_recibido > nodo) {
                        Cola.add(nodo_recibido);
                    } else {
                        synchronized (o) {
                            envia_Ok(reloj_logico, hosts[nodo_recibido], ports[nodo_recibido]);
                        }

                    }
                }
            }
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    private static void printCola() {
        if (Cola.size() > 0) {
            System.out.println("Cola:" + Cola);
            System.out.println();
        }
    }

    private static void lamport(long tiempo_recibido) {
        if (reloj_logico < tiempo_recibido) {
            synchronized (o) {
                reloj_logico = tiempo_recibido + 1;
            }
        }
    }

    private static boolean revisaConexiones() {
        for (int i = 0; i < num_nodos; i++) {
            envia_Barrera(hosts[i], ports[i]);
        }
        return true;
    }

    static void read(DataInputStream f, byte[] b, int posicion, int longitud) throws Exception {
        while (longitud > 0) {
            int n = f.read(b, posicion, longitud);
            posicion += n;
            longitud -= n;
        }
    }

}
