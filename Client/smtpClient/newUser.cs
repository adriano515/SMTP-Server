using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace smtpClient
{
    public partial class newUser : Form
    {
        serverConnection server = new serverConnection();
        public newUser()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (server.ResponseInt("new user:" + userText.Text + "pass:" + passText.Text + "", 250)) errorLabel.Text = "Usuario Creado con exito";
            else errorLabel.Text = "Error";
        }
    }
}
