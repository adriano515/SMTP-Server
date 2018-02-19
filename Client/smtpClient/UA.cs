using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net.Sockets;
using System.Text.RegularExpressions;
using System.Collections;
using System.IO;
using Newtonsoft.Json;

namespace smtpClient
{
    public partial class UA : Form
    {

        db db = new db();
        string mydocpath = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
        serverConnection server = new serverConnection("localhost", 2407);
        public UA()
        {
            
            InitializeComponent();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            Form1 form = new Form1();
            form.Show();
        }

        private void button4_Click(object sender, EventArgs e)
        {
            dataGridView1.DataSource = db.fillTable("wiichog");
            //newUser form = new newUser();
            //form.Show();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            if (server != null && server.ResponsePOP("APOP " + userTextbox.Text + "") && server.ResponsePOP("PASS " + passTextbox.Text + "")) {
                errorLabel.Text = "succesful login";
                LlenarGridview();
                userTextbox.Enabled = false;
                passTextbox.Enabled = false;
            }
            else { errorLabel.Text = "error on login"; }
            

        }

        private void button1_Click(object sender, EventArgs e)
        {
            LlenarGridview();
        }

        public void LlenarGridview() {
            List<String> list = server.ListCommand("list");
            for (int i = 0; i < list.Count(); i++)
            {
                List<String> mail = server.ListCommand("retr " + list[i].ToString());
                db.insert(list[i], mail[0], mail[1], mail[2], mail[3], "");
                dataGridView1.DataSource = db.fillTable("wiichog");
                server.Write("./n");
                server.Write("del " + list[i]);
            }
        }

        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            string emailId = dataGridView1.Rows[e.RowIndex].Cells[1].Value.ToString();
            List<String> data = db.getEmailData(emailId);
            fromLabel.Text = data[0];
            subjectLabel.Text = data[1];
            richTextBox1.Text = data[2];
        }
    }
}
