using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net;
using System.Net.Sockets;
using System.Text.RegularExpressions;

namespace smtpClient

{
    class serverConnection
    {
        public NetworkStream ns;
        public serverConnection(String ip, int port) {
            byte[] data = new byte[1024];
            try {
                TcpClient server = new TcpClient(ip, port);
                ns = server.GetStream();
                int recv = ns.Read(data, 0, data.Length);
            }
            catch (Exception e) {
                
            }
        }
               
        public bool Validate(String email)
        {
            if (Regex.Match(email, @"^([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)$").Success) return true;
            return false;
        }
        public void Write(String Command)
        {
            ns.Write(Encoding.ASCII.GetBytes(Command), 0, Command.Length);
        }

        public bool ResponseTCP(String Command, int number)
        {
            byte[] data = new byte[1024];
            ns.Write(Encoding.ASCII.GetBytes(Command), 0, Command.Length);
            int recv = ns.Read(data, 0, data.Length);
            int response = Int32.Parse(Encoding.ASCII.GetString(data, 0, recv).Split(' ')[0]);
            if (response == number) return true;
            return false;
        }

        public String ResponseString(String Command)
        {
            byte[] data = new byte[1024];
            ns.Write(Encoding.ASCII.GetBytes(Command), 0, Command.Length);
            int recv = ns.Read(data, 0, data.Length);
            String response = Encoding.ASCII.GetString(data, 0, recv);
            return response;
        }

        public bool ResponsePOP(String Command)
        {
            byte[] data = new byte[1024];
            ns.Write(Encoding.ASCII.GetBytes(Command), 0, Command.Length);
            int recv = ns.Read(data, 0, data.Length);
            String response = Encoding.ASCII.GetString(data, 0, recv).Split(' ')[0];
            if (response.Equals("+OK")) return true;
            return false;
        }

        public List<String> ListCommand(String Command) {
            byte[] data = new byte[1024];
            List<String> Identificator = new List<String>();
            ns.Write(Encoding.ASCII.GetBytes(Command), 0, Command.Length);
            while (true) {
                int recv = ns.Read(data, 0, data.Length);
                String response = Encoding.ASCII.GetString(data, 0, recv);
                try {
                    int identificator = Int32.Parse(response.Split(' ')[0]);
                    Identificator.Add(response);
                }
                catch (Exception e) {
                    if (response.Split(' ')[0].Equals(".")) {
                        return Identificator;
                    }
                    if (response.Split(':')[0].Equals("From ") || response.Split(':')[0].Equals("To ") || response.Split(':')[0].Equals("Data "))
                    {
                        Identificator.Add(response);
                    }

                }
            }
        }
    }
}
