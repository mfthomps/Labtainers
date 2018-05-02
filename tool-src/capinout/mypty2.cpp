/*
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
*/

/*
Capture stdin and stdout of selected programs into timestamped files.
Input arguments include:
    -- A command line, potentially including a pipe and redirection.
    -- An indication of which command within a piped stream is to be
       monitored. 0: there are no pipes
                  1: left side of pipe
                  2: right side of pipe
    -- A timestampe string   
    -- The full path to the command (used to determine if /etc/init.d
       programs are invoked.)
The program also detects use of systemctl, service and /etc/init.d to
monitor services.

When the command line indicates that the program to be monitored is 
will use the terminal, a pty is created and used by a master to catch
and record stdin & stdout.  If the program to be monitored is to the
right of a pipe, then pipes are used so that the pipe used by the
program to get its stdin can be closed without also closing the pipe
it uses for its stdout.
*/
#define _XOPEN_SOURCE 600
#include <stdlib.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <stdio.h>
#include <time.h>
#define __USE_BSD
#include <termios.h>
#include <sys/select.h>
#include <sys/ioctl.h>
#include <sys/wait.h>
#include <string.h>
#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include <cstring>
#include <algorithm>
#include <climits>
#include <sstream>
#include <iterator>
FILE *debug;
int fdm_in;
int fdm_out;
int stdout_fd, stdin_fd;
int pipe_fd[2];
int master_pipe_stdin[2];
int master_pipe_stdout[2];
int cmd_pid = 0;
int left_pid = 0;
int right_pid = 0;
int master_stdin = 0; 
int master_stdout = 1; 
int the_redirect_fd = -1;
int fds_in, fds_out;
int count_index = 1;
int ts_index = 2;
int cmd_path_index = 3;
struct termios orig_termios; 
struct termios latest_termios; 
bool use_pty = false;
char *trim(char *str)
{
       int tmp_trim = strlen(str)-1;
       while(tmp_trim >= 0 && str[tmp_trim] == ' '){
           str[tmp_trim] = 0;
           tmp_trim--;
       }
       while(str[0] == ' '){
           str++;
           if(*str == 0){
              return str;
           }
       }
       return str;
}
enum STR2INT_ERROR { SUCCESS, OVERFLOW, UNDERFLOW, INCONVERTIBLE };

STR2INT_ERROR str2int (int &i, char const *s, int base = 0)
{
    char *end;
    long  l;
    errno = 0;
    l = strtol(s, &end, base);
    if ((errno == ERANGE && l == LONG_MAX) || l > INT_MAX) {
        return OVERFLOW;
    }
    if ((errno == ERANGE && l == LONG_MIN) || l < INT_MIN) {
        return UNDERFLOW;
    }
    if (*s == '\0' || *end != '\0') {
        return INCONVERTIBLE;
    }
    i = l;
    return SUCCESS;
}
char *convert(const std::string & s)
{
   char *pc = new char[s.size()+1];
   std::strcpy(pc, s.c_str());
   return pc; 
}
using namespace std;

vector<string> split(const char *str, char c = ' ')
{
    vector<string> result;

    do
    {
        const char *begin = str;

        while(*str != c && *str)
            str++;

        result.push_back(string(begin, str));
    } while (0 != *str++);

    return result;
}
std::string join( const std::vector<std::string>& elements, const char* const separator)
{
    switch (elements.size())
    {
        case 0:
            return "";
        case 1:
            return elements[0];
        default:
            std::ostringstream os; 
            std::copy(elements.begin(), elements.end()-1, std::ostream_iterator<std::string>(os, separator));
            os << *elements.rbegin();
            return os.str();
    }
}
int getMaster()
{
   int rc;
   int fdm = posix_openpt(O_RDWR);
   if (fdm < 0)
   {
      fprintf(stderr, "Error %d on posix_openpt()\n", errno);
      return -1;
   }
   
   rc = grantpt(fdm);
   if (rc != 0)
   {
      fprintf(stderr, "Error %d on grantpt()\n", errno);
      return -1;
   }
   
   rc = unlockpt(fdm);
   if (rc != 0)
   {
      fprintf(stderr, "Error %d on unlockpt()\n", errno);
      return -1;
   }
   return fdm;
}
char **getCharFromVector(std::vector<std::string> sv)
{
    std::vector<char*> vc;
    std::transform(sv.begin(), sv.end(), std::back_inserter(vc), convert);
    char **my_args = (char **)malloc(sizeof(char *) * (vc.size()+1));
    for(int i=0; i<vc.size(); i++)
    { 
        my_args[i] = vc[i];
    }
    my_args[vc.size()] = 0;
    return my_args;
}
char **getExecArgs(char *cmd_args){
     char **my_args = (char **)malloc(sizeof(char *) * (4));
     my_args[0] = "sh";
     my_args[1] = cmd_args;
     my_args[2] = 0;
     return my_args;
}
char **getExecCmdArgs(char *cmd_args){
     std::vector<std::string> cmd_v = split(cmd_args);
     char **cmd_args_array = getCharFromVector(cmd_v);
     char **my_args = (char **)malloc(sizeof(char *) * (cmd_v.size()+2));
     fprintf(debug, "cmd size is %d\n", cmd_v.size());
     my_args[0] = "/sbin/exec_wrap.sh";
     for(int i=1; i<cmd_v.size()+1; i++){
         my_args[i] = cmd_args_array[i-1];
         fprintf(debug, "assigned myargs[%d] with %s\n", i, my_args[i]);
     }
     my_args[cmd_v.size()+1] = 0;
     fprintf(debug, "return my_args[1] is %s\n", my_args[1]);
     return my_args;
}
    
int forkLeft(int *pipe_fd, char *cmd){
       /*
       For use when monitored command is on right side of pipe.
       */
       int retval = fork();
       if (retval == 0){
           std::vector<std::string> left_args = split(cmd);
           // child map pipe to stdout
           close(1);
           dup2(pipe_fd[1], 1);
           close(pipe_fd[1]);
           close(pipe_fd[0]);
           char **my_args = getExecCmdArgs(cmd);
           fprintf(debug, "fork left now exec with [0] %s [1] %s \n", my_args[0], my_args[1]);
           fflush(debug);
           int rc = execvp(my_args[0], &my_args[0]);
           /* would be error if we get here */
           fprintf(debug, "execvp error rc is %d errno %d\n", rc, errno);
       }else{
           // parent.  master should read stdin from pipe
           close(pipe_fd[1]);
       }
       return retval;
}
int forkRight(int *pipe_fd, char *cmd){
       /*
       For use when monitored command is on left side of pipe.
       */
       int retval = fork();
       
       if (retval == 0){
           // child map pipe to stdin
           //std::vector<std::string> right_args = split(cmd);
           close(STDIN_FILENO);
           dup2(pipe_fd[0], STDIN_FILENO);
           close(pipe_fd[0]);
           close(pipe_fd[1]);
           char **my_args = getExecCmdArgs(cmd);
           fprintf(debug, "fork right now exec with [0] %s [1] %s \n", my_args[0], my_args[1]);
           fflush(debug);
           int rc = execvp(my_args[0], &my_args[0]);
           /* would be error if we get here */
           fprintf(debug, "execvp error rc is %d errno %d\n", rc, errno);
       }else{
           fprintf(debug, "forkRight, in parent, close unused pipe\n");
           // parent.  master should write stdout to pipe
           // close unused read side
           close(pipe_fd[0]);
       }
       return retval;
}
int handleRedirect(char *redirect_filename, char *append_filename){
     /* redirect stdout if needed */
     int retval = -1;
     if(redirect_filename != NULL){
         int redirect_fd = open(redirect_filename, O_RDWR | O_CREAT, 0644);
         if(redirect_fd < 0){
             fprintf(debug, "could not open redirect file %s\n", redirect_filename);
             return -1;
         }
         close(1);
         dup2(redirect_fd, 1);
         //close(redirect_fd);
         char string[] = "handleRedirect, wtf, over?\n";
         write(1, string, (strlen(string)+1));
         fprintf(debug, "redirect stdout to %s fd: %d\n", redirect_filename, redirect_fd);
         retval = redirect_fd;
     }else if(append_filename != NULL){
         int append_fd = open(append_filename, O_RDWR | O_APPEND);
         if(append_fd < 0){
             append_fd = open(append_filename, O_RDWR | O_CREAT, 0644);
             if(append_fd < 0){
                 fprintf(stderr, "could not open append file %s\n", append_filename);
                 return -1;
             }
         }
         close(1);
         dup2(append_fd, 1);
         retval = append_fd;
         //close(append_fd);
     }else{
         fprintf(debug, "No redirect\n");
     }
     return retval;
}
bool termsEqual(const struct termios one, const struct termios two)
{
  if(one.c_iflag != two.c_iflag || one.c_oflag != two.c_oflag || one.c_lflag != two.c_lflag)
  {
      return false;
  }else{
      return true;
  }
}
int closeUpShop(){
   time_t rawtime;
   struct tm * timeinfo;
   char buffer [80];
   time (&rawtime);
   timeinfo = localtime (&rawtime);
   strftime (buffer,80,"PROGRAM:FINISH %Y%m%d%H%M%S",timeinfo);
   write(stdin_fd, buffer, strlen(buffer));
   write(stdout_fd, buffer, strlen(buffer));
   close(stdout_fd);
   close(stdin_fd);
   close(master_stdout);
   if(the_redirect_fd > 0){
      close(the_redirect_fd);
   }
   tcsetattr (0, TCSANOW, &orig_termios);
}
int ioLoop()
{
     char input[150];
     fd_set fd_in;
     int rc;
     int tmp_count = 0;
     char eot = 0x04;
     struct termios attr; 
     while (1)
     {
       int stat;
       //if(use_pty && cmd_pid != 0){
       if(cmd_pid != 0){
          int wait_cmd = waitpid(cmd_pid, &stat, WNOHANG);
          fprintf(debug, "cmd_pid: %d wait_cmd got %d stat %d\n", cmd_pid, wait_cmd, stat);
          if(wait_cmd == cmd_pid)
          {
              fprintf(debug, "MATCHED, cmd_pid gone \n");
              close(fds_in);
       
          }
       }
       if(left_pid != 0){
          int wait_left = waitpid(left_pid, &stat, WNOHANG);
          fprintf(debug, "left_pid: %d wait_left got %d stat %d\n", left_pid, wait_left, stat);
          if(wait_left == left_pid)
          {
              fprintf(debug, "MATCHED\n");
              left_pid = 0;
              close(fdm_in);
              master_stdin = -1;
          }
          tmp_count++;
          if(tmp_count > 100){
              fprintf(debug, "too much, break\n");
              break;
          }
       }
       // Wait for data from standard input and master side of PTY
       FD_ZERO(&fd_in);
       if(master_stdin >=0 ){
           FD_SET(master_stdin, &fd_in);
       }else{
           fprintf(debug,"master_stdin closed, do not select on it\n");
       }
       fflush(debug);
       FD_SET(fdm_out, &fd_in);
       int max_fd = max(fdm_out, master_stdin);
       rc = select(max_fd + 1, &fd_in, NULL, NULL, NULL);
       fprintf(debug, "select returns %d\n", rc);
       fflush(debug);
       tcgetattr(fds_in, &attr);
       if(use_pty && !termsEqual(latest_termios, attr))
       {
           fprintf(debug,"pty terminal settings changed, change ours\n");
           tcsetattr (0, TCSANOW, &attr);
           latest_termios = attr;
           fprintf(debug, "term iflag %d oflag %d cflag %d lflag %d\n", attr.c_iflag, attr.c_oflag, attr.c_cflag, attr.c_lflag);
       }
       switch(rc)
       {
         case -1 : fprintf(debug, "Error %d on select()\n", errno);
                   if(errno != 4)
                   {
                       closeUpShop();
                       exit(0);
                   }
   
         default :
         {
             // If data on standard input
             if (master_stdin >= 0 && FD_ISSET(master_stdin, &fd_in)) {
                 rc = read(master_stdin, input, sizeof(input));
                 fprintf(debug, "read master_stdin rc is %d\n", rc);
                 if (rc > 0) {
                   // Send data on the master side of PTY
                   input[rc] = 0;
                   fprintf(debug, "read master_stdin %s\n", input);
                   write(fdm_in, input, rc);
                   write(stdin_fd, input, rc);
                   fprintf(debug, "read master_stdin, wrote to fdm_in %s\n", input);
                 } else {
                   if (rc < 0) {
                     fprintf(debug, "Error %d on read standard input\n", errno);
                     closeUpShop();
                     exit(0);
                   }
                 }
             }
     
             // If data on master side of PTY
             if (FD_ISSET(fdm_out, &fd_in))
             {
                  rc = read(fdm_out, input, sizeof(input));
                  fprintf(debug, "read fdm_out rc is %d\n", rc);
                  fflush(debug);
                  if (rc > 0)
                  {
                      // Send data on standard output
                      write(master_stdout, input, rc);
                      write(stdout_fd, input, rc);
                      input[rc] = 0;
                      fprintf(debug, "fdm_out got %s\n", input);
                  } else {
                      if (rc < 0) {
                          fprintf(debug, "Read zip (error %d) on read master PTY\n", errno);
                          //sleep(2);
                          closeUpShop();
                          int status;
                          int cpid;
                          fflush(debug);
                          if(right_pid != 0){
                              fprintf(debug, "wait for right side?\n");
                              fflush(debug);
                              while((cpid=wait(&status)) != right_pid){
                                  fprintf(debug, "got cpid of %d, status %d\n", cpid, status);
                              } 
                              fprintf(debug, "right side finished\n");
                              fflush(debug);
                          }
                          close(0);
                          close(1);
                          return 0;
                         
                      }else{
                          fprintf(debug,"read zero from fdm_out, assume pipe closed, and clean up\n");
                          closeUpShop();
                          exit(0);
                      }
                  }
              }
           }
       } // End switch
     } // End while
     return 0;
}
void sighandler(int signo)
{
    char etx = 0x03;
    fprintf(debug,"capinout got signal %d\n", signo);
    if(signo == SIGINT){
        fprintf(debug,"capinout got SIGINT\n");
    }
    if(cmd_pid != 0){
        fprintf(debug, "kill cmd\n");
        //write(fdm_in, &etx, 1);
        kill(cmd_pid, signo);
    }
    if(left_pid != 0){
        fprintf(debug, "kill left\n");
        kill(left_pid, signo);
    }
    if(right_pid != 0){
        fprintf(debug, "kill right \n");
        kill(right_pid, signo);
    }
    fprintf(debug, "no do loop again\n");
    fflush(debug);
    ioLoop();
    return;
}
void getStdInOutFiles(std::vector<std::string> cmd_args, std::vector<std::string> all_args, std::string *stdinfile, std::string *stdoutfile)
{
   char *precmd_home = std::getenv("PRECMD_HOME"); 
   if(precmd_home == NULL || strlen(precmd_home) == 0){
      fprintf(stderr, "PRECMD_HOME not defined\n");
      exit(1);
   }
   std::string initd_prefix  = "/etc/init.d";
   std::string time_stamp_in = ".stdin."+all_args[ts_index];
   std::string time_stamp_out = ".stdout."+all_args[ts_index];
   int prog_index = 0;  
   if(cmd_args[0] == "sudo"){
        //cout << "yep is sudo\n";
        prog_index = 1;
   }
   if(cmd_args[prog_index] == "systemctl"){
       // systemctl action program
       fprintf(debug, "is systemctl\n");
       time_stamp_in = ".service"+time_stamp_in;
       time_stamp_out = ".service"+time_stamp_out;
       prog_index += 2;
   }else if(cmd_args[prog_index] == "service"){
       // service program action
       fprintf(debug, "is service\n");
       time_stamp_in = ".service"+time_stamp_in;
       time_stamp_out = ".service"+time_stamp_out;
       prog_index ++;
   }else if(!all_args[cmd_path_index].compare(0, initd_prefix.size(), initd_prefix)){
       // /etc/init.d/program action
       fprintf(debug, "is /etc/init.d\n");
       time_stamp_in = ".service"+time_stamp_in;
       time_stamp_out = ".service"+time_stamp_out;
   }
       
   const char *prog_char = cmd_args[prog_index].c_str();
   char *prog_base = basename((char *)prog_char);

   /* get stdin & stdout capture file names */
   std::string local_result = "/.local/result/";
   fprintf(debug, "prog_base is %s precmd_home is %s\n", prog_base, precmd_home);
   *stdinfile = std::string(precmd_home) + local_result + std::string(prog_base) + time_stamp_in;
   *stdoutfile = std::string(precmd_home) + local_result + std::string(prog_base) + time_stamp_out;
   // cout << "stdinfile "+stdinfile+"\n";
}
int main(int argc, char *argv[])
{
   int rc;
   std::string stdinfile;
   std::string stdoutfile;
   // Check arguments
   if (argc <= ts_index)
   {
       fprintf(stderr, "Usage: %s cmd_line count timestamp\n", argv[0]);
       exit(1);
   }
   debug = fopen("/tmp/capinout_debug.out", "w");
   if(signal(SIGINT, sighandler) == SIG_ERR){
       fprintf(stderr, "error setting SIGINT signal handler\n");
   }
   tcgetattr(0, &orig_termios);

   std::string first_arg;
   std::vector<std::string> all_args;
   if (argc > 1) {
     first_arg = argv[1];
     all_args.assign(argv + 1, argv + argc);
   }

   char *cmd = argv[1];
   /* look for redirect/append */
   char *append_filename = NULL;
   char *redirect_filename = NULL;
   char* append_str = strstr(argv[1],">>");
   if(append_str != NULL)
   {
       int append_index = append_str - argv[1];
       cmd = strdup(argv[1]);
       cmd[append_index] = 0;
       append_filename = argv[1]+append_index+1; 
       append_filename = trim(append_filename);
       fprintf(debug, "append_filename %s\n", append_filename);
   }else{ 
       /* look for redirect */
       char* redirect_str = strstr(argv[1],">");
       if(redirect_str != NULL)
       {
           int redirect_index = redirect_str - argv[1];
           cmd = strdup(argv[1]);
           cmd[redirect_index] = 0;
           redirect_filename = argv[1]+redirect_index+1; 
           redirect_filename = trim(redirect_filename);
           fprintf(debug, "redirect_filename %s\n", redirect_filename);
       } 
   }

   /* cmd should not be free of redirects.  Look for pipes */
   fprintf(debug, "cmd now %s\n",cmd);
   fflush(debug);
   char *cmd_exec_args = NULL;
   char *right_side = NULL;
   char *pipe_str = strstr(cmd, "|");
   if(pipe_str != NULL)
   {
       int pipe_index = pipe_str - cmd;
       cmd = strdup(cmd);
       cmd[pipe_index] = 0;
       right_side = cmd+pipe_index+1; 
       right_side = trim(right_side);
       cmd = trim(cmd);
       fprintf(debug, "right side: [%s], left [%s]\n", right_side, cmd);
   }
   /* cmd is left side of pipe, right_side is right (if any) */
   std::vector<std::string> cmd_args;

   int count;
   const char *count_str = all_args[count_index].c_str();
   rc = str2int(count, all_args[count_index].c_str()); 
   fprintf(debug, "count is %d\n", count);

   if(count == 2)
   {
       /* cmd is on right of pipe.  exec left side wth new pipe as stdout */
       if(right_side == NULL){
           fprintf(stderr, "Got pipe count of two, but no pipe %s\n", cmd);
           return 1;
       }
       cmd_args = split(right_side);
       fprintf(debug, "was right side, cmd_args[0] is [%s]\n", cmd_args[0].c_str());
       cmd_exec_args = right_side;
   }else{
       cmd_args = split(cmd);
       fprintf(debug, "was left side, cmd_args[0] is [%s]\n", cmd_args[0].c_str());
       cmd_exec_args = cmd;
   }

   getStdInOutFiles(cmd_args, all_args, &stdinfile, &stdoutfile);
   if(count != 2)
   {
      use_pty = true;
      fdm_in = getMaster();
      if(fdm_in < 0){
          return 1;
      }   
      fdm_out = fdm_in;
      // Open the slave side ot the PTY
      fds_in = open(ptsname(fdm_in), O_RDWR);
      fds_out = fds_in;
   }else{
      use_pty = false;
      // master write stdin to this for slave to consume
      pipe(master_pipe_stdin);
      // master reads stdout from slave
      pipe(master_pipe_stdout);

      // master writes stdin to slave
      fdm_in = master_pipe_stdin[1]; 
      // master reads stdout from slave
      fdm_out = master_pipe_stdout[0]; 

      // slave reads stdin from master
      fds_in = master_pipe_stdin[0]; 
      // slave write stdout to master
      fds_out = master_pipe_stdout[1]; 
   }
   if(count == 2){
         pipe(pipe_fd);
         left_pid = forkLeft(pipe_fd, cmd);
         master_stdin = pipe_fd[0];
         fprintf(debug, "back from forkLeft, pid is %d  master_stdin is %d\n", left_pid, master_stdin);
   }
   
   // Create the child process
   cmd_pid = fork();
   if (cmd_pid)
   {
     // parent
     if(!use_pty){ 
        // Close the slave side of the PTY or pipe
        if(count != 2){
           close(fds_in);
        }else{
           close(fds_in);
           close(fds_out);
        }
     }
     stdin_fd = open(stdinfile.c_str(), O_RDWR | O_CREAT, 0644);
     if(stdin_fd <=0 ){
         fprintf(stderr, "Could not open %s for writing. %d\n", stdinfile.c_str(), errno);
         return 1;
     } 
     char tmp_buf[] = "PROGRAM_ARGUMENTS is ";
     char newline[] = "\n";
     write(stdin_fd, tmp_buf, strlen(tmp_buf));
     write(stdin_fd, argv[1], strlen(argv[1]));
     write(stdin_fd, newline, 1);

     stdout_fd = open(stdoutfile.c_str(), O_RDWR | O_CREAT, 0644);
     /* redirect stdout if needed */
     if((count == 0 || count == 2) && (redirect_filename != NULL || append_filename != NULL)){
        /* no pipe or monitored command is on right of pipe */
        the_redirect_fd = handleRedirect(redirect_filename, append_filename);
        if(the_redirect_fd < 0){
            fprintf(stderr, "error from handleRedirect, exit\n");
            return 1;
        }
        master_stdout = the_redirect_fd; 
     }else if(count == 1){
        pipe(pipe_fd);
        right_pid = forkRight(pipe_fd, right_side);     
        if(strstr(right_side, "less") == right_side)
        {
            fprintf(debug, "IS LESS\n");
        }
        master_stdout = pipe_fd[1];
        fprintf(debug, "Forked right pid is %d, master std out should go to pipe %d\n", right_pid, master_stdout);
     }
     fprintf(debug, "about to loop, master_stdin: %d  master_stdout: %d\n", master_stdin, master_stdout);
     return(ioLoop());
   } else {
   
     // CHILD
     if(count != 2)
     { 
        // Close the master side of the PTY
        close(fdm_in);
   
        // match the pty to our original terminal settings
        tcsetattr (fds_in, TCSANOW, &orig_termios);
        latest_termios = orig_termios;
     }else{
        close(fdm_in);
        close(fdm_out);
     }
   
     // The slave side of the PTY becomes the standard input and outputs of the child process
     close(0); // Close standard input (current terminal)
     close(1); // Close standard output (current terminal)
     close(2); // Close standard error (current terminal)
   
     dup(fds_in); // PTY becomes standard input (0)
     dup(fds_out); // PTY becomes standard output (1)
     dup(fds_out); // PTY becomes standard error (2)
  
     if(count != 2)
     { 
        // Now the original file descriptor is useless
        close(fds_in);
   
        // Make the current process a new session leader
        setsid();
   
        // As the child is a session leader, set the controlling terminal to be the slave side of the PTY
        // (Mandatory for programs like the shell to make them manage correctly their outputs)
        ioctl(0, TIOCSCTTY, 1);
     }
   
     // Execution of the program

     /*
     Get the exec arguments
     */
     char **my_args = getExecCmdArgs(cmd_exec_args);
     //fprintf(debug, "fork command, now exec with [0] %s [1] %s [2] %s\n", my_args[0], my_args[1], my_args[2]);
     fprintf(debug, "fork command, now exec with [0] %s \n", my_args[0]);
     fflush(debug);
     rc = execvp(my_args[0], &my_args[0]);

     /* would be error if we get here */
     fprintf(debug, "execvp error rc is %d errno %d\n", rc, errno);

     
     return 1;
   }
   
   return 0;
} // main
