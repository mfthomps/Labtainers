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
FILE *debug;
int fdm;
int stdout_fd, stdin_fd;
int pipe_fd[2];
int left_pid = 0;
int right_pid = 0;
int master_stdin = 0; 
int master_stdout = 1; 
int the_redirect_fd = -1;
int count_index = 1;
int ts_index = 2;
int cmd_path_index = 3;
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
           //char string[] = "hey there\n";
           //write(1, string, (strlen(string)+1));
           std::vector<char*> left_exec_args;
           std::transform(left_args.begin(), left_args.end(), std::back_inserter(left_exec_args), convert);   
           char **my_args = (char **)malloc(sizeof(char *) * left_exec_args.size()+1);
           for(int i=0; i<left_exec_args.size(); i++){
               fprintf(debug, "arg %d is %s\n", i, left_exec_args[i]);
               my_args[i] = left_exec_args[i];
           }
           my_args[left_exec_args.size()] = 0;
           fprintf(debug, "now exec with left_exec_args[0] is %s\n", left_exec_args[0]);
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
           std::vector<std::string> right_args = split(cmd);
           close(STDIN_FILENO);
           dup2(pipe_fd[0], STDIN_FILENO);
           close(pipe_fd[0]);
           close(pipe_fd[1]);
           //char string[] = "hey there\n";
           //write(1, string, (strlen(string)+1));
           std::vector<char*> right_exec_args;
           std::transform(right_args.begin(), right_args.end(), std::back_inserter(right_exec_args), convert);   
           char **my_args = (char **)malloc(sizeof(char *) * right_exec_args.size()+1);
           for(int i=0; i<right_exec_args.size(); i++){
               fprintf(debug, "arg %d is %s\n", i, right_exec_args[i]);
               my_args[i] = right_exec_args[i];
           }
           my_args[right_exec_args.size()] = 0;
           fprintf(debug, "now exec with right_exec_args[0] is %s\n", right_exec_args[0]);
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
         char string[] = "wtf, over?\n";
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
int closeUpShop(int stdin_fd, int stdout_fd){
   time_t rawtime;
   struct tm * timeinfo;
   char buffer [80];
   time (&rawtime);
   timeinfo = localtime (&rawtime);
   strftime (buffer,80,"PROGRAM:FINISH %Y%m%d%H%M%S",timeinfo);
   write(stdin_fd, buffer, strlen(buffer));
   write(stdout_fd, buffer, strlen(buffer));
}
int ioLoop()
{
     char input[150];
     fd_set fd_in;
     int rc;
     while (1)
     {
       // Wait for data from standard input and master side of PTY
       FD_ZERO(&fd_in);
       FD_SET(master_stdin, &fd_in);
       FD_SET(fdm, &fd_in);
       int max_fd = max(fdm, master_stdin);
       rc = select(max_fd + 1, &fd_in, NULL, NULL, NULL);
       switch(rc)
       {
         case -1 : fprintf(debug, "Error %d on select()\n", errno);
                   closeUpShop(stdin_fd, stdout_fd);
                   exit(0);
   
         default :
         {
             // If data on standard input
             if (FD_ISSET(master_stdin, &fd_in)) {
                 rc = read(master_stdin, input, sizeof(input));
                 if (rc > 0) {
                   // Send data on the master side of PTY
                   fprintf(debug, "read master_stdin %s\n", input);
                   write(fdm, input, rc);
                   write(stdin_fd, input, rc);
                 } else {
                   if (rc < 0) {
                     fprintf(debug, "Error %d on read standard input\n", errno);
                     closeUpShop(stdin_fd, stdout_fd);
                     exit(0);
                   }
                 }
             }
     
             // If data on master side of PTY
             if (FD_ISSET(fdm, &fd_in))
             {
                  rc = read(fdm, input, sizeof(input));
                  if (rc > 0)
                  {
                      // Send data on standard output
                      write(master_stdout, input, rc);
                      write(stdout_fd, input, rc);
                  } else {
                      if (rc < 0) {
                          fprintf(debug, "Read zip (error %d) on read master PTY\n", errno);
                          closeUpShop(stdin_fd, stdout_fd);
                          close(stdout_fd);
                          close(stdin_fd);
                          close(master_stdout);
                          if(the_redirect_fd > 0){
                              close(the_redirect_fd);
                          }
                          close(stdin_fd);
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
    fprintf(debug,"got signal %d\n", signo);
    if(signo == SIGINT){
        fprintf(debug,"got SIGINT\n");
        fflush(debug);
    }
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
       time_stamp_in = "service."+time_stamp_in;
       time_stamp_out = "service."+time_stamp_out;
       prog_index += 2;
   }else if(cmd_args[prog_index] == "service"){
       // service program action
       fprintf(debug, "is service\n");
       time_stamp_in = "service."+time_stamp_in;
       time_stamp_out = "service."+time_stamp_out;
       prog_index ++;
   }else if(!all_args[cmd_path_index].compare(0, initd_prefix.size(), initd_prefix)){
       // /etc/init.d/program action
       fprintf(debug, "is /etc/init.d\n");
       time_stamp_in = "service."+time_stamp_in;
       time_stamp_out = "service."+time_stamp_out;
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
   int fds;
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
   }else{
       cmd_args = split(cmd);
       fprintf(debug, "was left side, cmd_args[0] is [%s]\n", cmd_args[0].c_str());
   }

   getStdInOutFiles(cmd_args, all_args, &stdinfile, &stdoutfile);

   fdm = getMaster();
   if(fdm < 0){
       return 1;
   }   
   // Open the slave side ot the PTY
   fds = open(ptsname(fdm), O_RDWR);
   
   // Create the child process
   if (fork())
   {
   
     // parent
   
     // Close the slave side of the PTY
     close(fds);
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
     if(count == 2){
         pipe(pipe_fd);
         left_pid = forkLeft(pipe_fd, cmd);
         master_stdin = pipe_fd[0];
         fprintf(debug, "back from forkLeft, pid is %d  master_stdin is %d\n", left_pid, master_stdin);
     }
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
     struct termios slave_orig_term_settings; // Saved terminal settings
     struct termios new_term_settings; // Current terminal settings
   
     // CHILD
   
     // Close the master side of the PTY
     close(fdm);
   
     // Save the defaults parameters of the slave side of the PTY
     rc = tcgetattr(fds, &slave_orig_term_settings);
   
     // Set RAW mode on slave side of PTY
     new_term_settings = slave_orig_term_settings;
     cfmakeraw (&new_term_settings);
     tcsetattr (fds, TCSANOW, &new_term_settings);
   
     // The slave side of the PTY becomes the standard input and outputs of the child process
     close(0); // Close standard input (current terminal)
     close(1); // Close standard output (current terminal)
     close(2); // Close standard error (current terminal)
   
     dup(fds); // PTY becomes standard input (0)
     dup(fds); // PTY becomes standard output (1)
     dup(fds); // PTY becomes standard error (2)
   
     // Now the original file descriptor is useless
     close(fds);
   
     // Make the current process a new session leader
     setsid();
   
     // As the child is a session leader, set the controlling terminal to be the slave side of the PTY
     // (Mandatory for programs like the shell to make them manage correctly their outputs)
     ioctl(0, TIOCSCTTY, 1);
   
     // Execution of the program

     /*
     Get the exec arguments
     */
     std::vector<char*> exec_args;
     std::transform(cmd_args.begin(), cmd_args.end(), std::back_inserter(exec_args), convert);   
     char **my_args = (char **)malloc(sizeof(char *) * exec_args.size()+1);
     for(int i=0; i<exec_args.size(); i++){
         fprintf(debug, "arg %d is %s\n", i, exec_args[i]);
         my_args[i] = exec_args[i];
     }
     my_args[exec_args.size()] = 0;

     fprintf(debug, "now exec with exec_args[0] is %s\n", exec_args[0]);
     rc = execvp(my_args[0], &my_args[0]);
     /* would be error if we get here */
     fprintf(debug, "execvp error rc is %d errno %d\n", rc, errno);

     
     return 1;
   }
   
   return 0;
} // main
