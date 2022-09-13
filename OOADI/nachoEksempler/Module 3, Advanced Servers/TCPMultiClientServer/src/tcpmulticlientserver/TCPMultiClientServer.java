/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package tcpmulticlientserver;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

/**
 *
 * @author irl
 */
public class TCPMultiClientServer {

    /**
     * @param args the command line arguments
     * @throws java.io.IOException
     */
    public static void main(String[] args) throws IOException {
        // TODO code application logic here
        System.out.println("Threaded Server is Running and listening on port 9999...." );
        ServerSocket mysocket = new ServerSocket(9999);
        
        while(true){
            Socket sock = mysocket.accept();
            ServerThread server=new ServerThread(sock);
 
            Thread serverThread=new Thread(server);
            serverThread.start();

         }
      }
        
}