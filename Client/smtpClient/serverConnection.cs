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
        public TcpClient server;
        public bool Validate(String email)
        {
            if (Regex.Match(email, @"^([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)$").Success) return true;
            return false;
        }
        public void Write(String Command)
        {
            ns.Write(Encoding.ASCII.GetBytes(Command), 0, Command.Length);
        }
        public bool Connect(String ip, int port)
        {
            byte[] data = new byte[1024];
            try
            {
                server = new TcpClient(ip, port);
                ns = server.GetStream();
                int recv = ns.Read(data, 0, data.Length);
                if (Int32.Parse(Encoding.ASCII.GetString(data, 0, recv).Split(' ')[0]) == 220) return true;
                return false;
            }
            catch (Exception e)
            {
                return false;
            }
        }

        public bool ResponseInt(String Command, int number)
        {
            byte[] data = new byte[1024];
            ns.Write(Encoding.ASCII.GetBytes(Command), 0, Command.Length);
            int recv = ns.Read(data, 0, data.Length);
            int response = Int32.Parse(Encoding.ASCII.GetString(data, 0, recv).Split(' ')[0]);
            if (response == 250) return true;
            else if (response == 354) return true;
            else if (response == 221) return true;
            return false;
        }
    }
}
