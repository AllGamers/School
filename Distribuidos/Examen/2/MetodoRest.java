import java.net.URL;
import java.net.HttpURLConnection;
import java.net.URLEncoder;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;

class MetodoRest{

	static class Usuario{
		int id_usuario;
		String email;
		String nombre;
		String apellido_paterno;
		String apellido_materno;
		String fecha_nacimiento;
		String telefono;
		String genero;
		byte[] foto;
	}

	public static void main(String[] args) throws Exception{
		URL url = new URL("http://sisdis.sytes.net:8080/Servicio/rest/ws/calcular");
		HttpURLConnection conexion = (HttpURLConnection) url.openConnection();
		conexion.setDoOutput(true);
		conexion.setRequestMethod("POST");
		conexion.setRequestProperty("Content-Type","application/x-www-form-urlencoded");
		String parametros = "p1=" + URLEncoder.encode("17.7265","UTF-8")+"&p2="+URLEncoder.encode("76.3144","UTF-8")+"&p3="+URLEncoder.encode("75.8464","UTF-8")+"&p4="+URLEncoder.encode("3.3496","UTF-8");
		//String parametros = "a=" + URLEncoder.encode("21","UTF-8");
		
		OutputStream os = conexion.getOutputStream();

		os.write(parametros.getBytes());
		os.flush();

		if(conexion.getResponseCode()==200){
			BufferedReader br = new BufferedReader(new InputStreamReader((conexion.getInputStream())));
			String respuesta;
			while ((respuesta = br.readLine()) != null){
				System.out.println(respuesta);
			}
		}else{
			BufferedReader br = new BufferedReader(new InputStreamReader((conexion.getErrorStream())));
			String respuesta;
			while ((respuesta = br.readLine()) != null) System.out.println(respuesta);
		}

		conexion.disconnect();
	}
}
	