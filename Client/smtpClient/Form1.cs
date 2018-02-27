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
        public TcpClient serverConnection;
        serverConnection server = new serverConnection("192.168.43.17",2407);
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            String[] emails = toEmail.Text.Split(',');
            DateTime thisDay = DateTime.Today;
            String[] message = dataTextbox.Text.Split('\n');
            if (emails.All(a=> server.Validate(a))) {
                if (server.ResponseTCP("HELO relay.example.com",250) && server.ResponseTCP("MAIL FROM: <bob@example.com>",250) && Array.TrueForAll(emails, email => { return server.ResponseTCP("RCPT TO: <" + email + ">", 250); }) && server.ResponseTCP("DATA\n",354))
                {
                    server.Write("From:<bat14074gar14189@example.com>");
                    server.Write("To: "+ String.Join(",", (from email in Enumerable.Range(0, emails.Length) select "<" + emails[email] + ">")).ToString() + "");
                    server.Write("Date: " + thisDay.ToString() + "");
                    server.Write("Subject: "+ subjectText.Text +"");
                    server.Write("\n");
                    Array.ForEach(message, element => server.Write(element));
                    if (server.ResponseTCP(".\n",250) && server.ResponseTCP("QUIT",221)) {
                        emailErrorLabel.Text = "Email Sent";
                        toEmail.Text = "";
                        subjectText.Text = "";
                        dataTextbox.Text = "";
                        server.ns.Close();
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
            if (server!=null){
                toEmail.Enabled = true;
                subjectText.Enabled = true;
                dataTextbox.Enabled = true;
                sendMessage.Enabled = true;
                ipTextbox.Enabled = false;
                portTextbox.Enabled = false;
                connectButton.Enabled = false;
            }
        }
        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void button1_Click_2(object sender, EventArgs e)
        {
            this.Close();
        }
    }
}
