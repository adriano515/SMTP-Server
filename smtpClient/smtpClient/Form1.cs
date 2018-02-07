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
    public partial class Form1 : Form
    {
        NetworkStream ns;
        TcpClient server;
        public Form1()
        {
            InitializeComponent();
        }

        public bool Validate(String email) {
            if (Regex.Match(email, @"^([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)$").Success) return true;
            return false;
        }
        public bool Connect(String ip, int port) {
            byte[] data = new byte[1024];
            try
            {
                server = new TcpClient(ip, port);
                ns = server.GetStream();
                int recv = ns.Read(data, 0, data.Length);
                if (Int32.Parse(Encoding.ASCII.GetString(data, 0, recv).Split(' ')[0]) == 220) return true;
                return false;
            }
            catch (Exception e) {
                return false;
            }
        }

        public int Response(String Command) {
            byte[] data = new byte[1024];
            ns.Write(Encoding.ASCII.GetBytes(Command), 0, Command.Length);
            int recv = ns.Read(data, 0, data.Length);
            return Int32.Parse(Encoding.ASCII.GetString(data, 0, recv).Split(' ')[0]);
        }
        public void Write(String Command) {
            ns.Write(Encoding.ASCII.GetBytes(Command), 0, Command.Length);
        }
        private void button1_Click(object sender, EventArgs e)
        {
            String[] emails = toEmail.Text.Split(',');
            String[] message = dataTextbox.Text.Split('\n');
            if (emails.All(a=>Validate(a))) {
                if (Response("HELO relay.example.com") == 250 && Response("MAIL FROM: <bob@example.com>") == 250 && Response("RCPT TO: <alice@example.com>") == 250 && Response("DATA\n") == 354)
                {
                    Write("From: " + "bat14074gar14189" + " <bat14074gar14189@example.com>");
                    Write("To: Alice Example <"+ String.Join(",", (from email in Enumerable.Range(0, emails.Length) select "<" + emails[email] + ">")).ToString() + ">");
                    Write("Subject: "+ subjectText.Text +"");
                    Write("\n");
                    Array.ForEach(message, element => Write(element));
                    if (Response(".") == 250 && Response("QUIT") == 221) {
                        emailErrorLabel.Text = "Email Sent";
                        ns.Close();
                        server.Close();
                    }
                }
            }

        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void label5_Click(object sender, EventArgs e)
        {

        }

        private void button1_Click_1(object sender, EventArgs e)
        {
            if(Connect(ipTextbox.Text, Int32.Parse(portTextbox.Text))){
                toEmail.Enabled = true;
                subjectText.Enabled = true;
                dataTextbox.Enabled = true;
                sendMessage.Enabled = true;
                attachButton.Enabled = true;
                ipTextbox.Enabled = false;
                portTextbox.Enabled = false;
                connectButton.Enabled = false;
            }
        }

        private void attachButton_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog1 = new OpenFileDialog();
            openFileDialog1.InitialDirectory = @"C:\";
            openFileDialog1.RestoreDirectory = true;
            openFileDialog1.Title = "Browse Text Files";
            openFileDialog1.Filter = "txt files (*.txt)|*.txt|All files (*.*)|*.*";
            openFileDialog1.FilterIndex = 2;
            openFileDialog1.DefaultExt = "txt";
            openFileDialog1.ShowDialog();
            emailErrorLabel.Text = openFileDialog1.FileName;
        }
    }
}
