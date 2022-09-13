/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package tcpmulticlientserver;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;

/**
 *
 * @author irl
 */
public class ServerThread implements Runnable{
    
    	Socket connectionSocket;
 
	public ServerThread(Socket s){
            try{
		connectionSocket=s;
            }catch(Exception e){}
	}
 
        @Override
	public void run(){
            try{
	        BufferedReader reader;
                reader =  new BufferedReader(new InputStreamReader(connectionSocket.getInputStream()));
		BufferedWriter writer;
                writer = new BufferedWriter(new OutputStreamWriter(connectionSocket.getOutputStream()));
 
                String ip=connectionSocket.getRemoteSocketAddress().toString();
                int port=connectionSocket.getPort();
                
                String line;
                
                line=reader.readLine();
                writer.write("Hi there, well done! this is what you sent: " + line + " from" + ip + "\n");
                writer.flush();
                System.out.println("Received connection from" + ip + "with text: "+ line +"\r");
                
                connectionSocket.close();
            
            }catch(IOException e){}
	}
    
}
