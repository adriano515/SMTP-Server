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
        serverConnection server = new serverConnection();
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            String[] emails = toEmail.Text.Split(',');
            DateTime thisDay = DateTime.Today;
            var rcptemails = Array.TrueForAll(emails, email => { return server.ResponseInt(email, 250);});
            String[] message = dataTextbox.Text.Split('\n');
            if (emails.All(a=> server.Validate(a))) {
                if (server.ResponseInt("HELO relay.example.com",250) && server.ResponseInt("MAIL FROM: <bob@example.com>",250) && rcptemails && server.ResponseInt("DATA\n",354))
                {
                    server.Write("From: " + "bat14074gar14189" + " <bat14074gar14189@example.com>");
                    server.Write("To: Alice Example "+ String.Join(",", (from email in Enumerable.Range(0, emails.Length) select "<" + emails[email] + ">")).ToString() + "");
                    server.Write("Date: " + thisDay.ToString() + "");
                    server.Write("Subject: "+ subjectText.Text +"");
                    server.Write("\n");
                    Array.ForEach(message, element => server.Write(element));
                    if (server.ResponseInt(".\n",250) && server.ResponseInt("QUIT",221)) {
                        emailErrorLabel.Text = "Email Sent";
                        server.ns.Close();
                        server.server.Close();
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
            if(server.Connect(ipTextbox.Text, Int32.Parse(portTextbox.Text))){
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

        private void Form1_Load(object sender, EventArgs e)
        {

        }
    }
}
