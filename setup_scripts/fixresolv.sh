#!/bin/bash
: <<'END'
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
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


Add the hosts DNS servers to the /etc/resolv.conf by appending them
to the resolv.conf.d/head file.  Some dockers, ubuntu?, cannot resolve
addresses from within containers.
END
rel=`lsb_release -a | grep Release | awk '{print $2}'`
if [[ $rel == 14.* ]]; then
    dns_list=$(nmcli dev list | grep DNS | awk '{print $2 $4}')
else
    dns_list=$(nmcli dev show | grep DNS | awk '{print $2 $4}')
fi
for dns in $dns_list
do
    already=$(grep $dns /etc/resolvconf/resolv.conf.d/head)
    if [ -z "$already" ]; then
        echo "nameserver $dns" | sudo tee -a /etc/resolvconf/resolv.conf.d/head
    fi
done
sudo resolvconf -u

# Verify /etc/resolv.conf
echo "resolveconf now contains:"
cat /etc/resolv.conf
