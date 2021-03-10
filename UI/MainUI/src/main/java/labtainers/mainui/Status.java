/*
This software was created by United States Government employees at 
The Center for Cybersecurity and Cyber Operations (C3O) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
*/

/*
Report on status of Docker containers using given labels and messages.
Running containers are named via strings matched to the output of "docker ps".
*/
package labtainers.mainui;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.Set;
import java.util.HashSet;
import java.util.ArrayList;


public class Status implements Runnable {
    private class StatusInfo{
       protected javax.swing.JLabel label;
       protected String message;
       protected String look_for;
       protected boolean was_running;
       protected boolean now_running;
       protected StatusInfo(javax.swing.JLabel label, String message, String look_for){
           this.label = label;
           this.message = message;
           this.look_for = look_for;
           this.was_running = false;
           this.now_running = false;
       }
   }
   private javax.swing.JLabel label;
   private String message;
   private ArrayList<String> look_for;
   private boolean was_running = false;
   private ArrayList<StatusInfo> status_info;
   
   public Status(javax.swing.JLabel label, String message, String look_for) {
      this.status_info = new ArrayList<StatusInfo>();
      StatusInfo stat = new StatusInfo(label, message, look_for);
      stat.label.setText(stat.message+" No");
      this.status_info.add(stat);
   }
   public void addLabel(javax.swing.JLabel label, String message, String look_for) {
      StatusInfo stat = new StatusInfo(label, message, look_for);
      stat.label.setText(stat.message+" No");
      this.status_info.add(stat);
   }
   public void changeLook(javax.swing.JLabel label, String look_for){
       for(StatusInfo stat : this.status_info){
           if(stat.label == label){
               stat.look_for = look_for;
               break;
           }
       }
   }
   
   public void run() {
      Set<String> running_set;
      boolean now_running;
      while(true) {
         isRunning();
         for(StatusInfo stat : this.status_info){
              if(stat.now_running &! stat.was_running){
                  stat.label.setText(stat.message+" Yes");
              }else if(!stat.now_running && stat.was_running){
                  stat.label.setText(stat.message+" No");
              }
              stat.was_running = stat.now_running;
         }
         try{
            Thread.sleep(2000);
         }catch(InterruptedException ex){
            System.out.println(ex);
         }
      }
   }
   private void isRunning(){
      String line;
      //Executable file name of the application to check. 
      
      try{
          Process proc = Runtime.getRuntime().exec("docker ps");
          InputStream stream = proc.getInputStream();
          BufferedReader reader = new BufferedReader(new InputStreamReader(stream));
          for(StatusInfo stat : this.status_info){
              stat.now_running = false;
          }
          while ((line = reader.readLine()) != null) {
              for(StatusInfo stat : this.status_info){
                  Pattern pattern = Pattern.compile(stat.look_for);
                  Matcher matcher = pattern.matcher(line);
                  if (matcher.find()) {
                      stat.now_running = true;
                  }
              }
          }
      }catch(IOException ex){
          System.out.println("Status error getting ps "+ex.toString());
      }
   }
}
