namespace smtpClient
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.toEmail = new System.Windows.Forms.TextBox();
            this.subjectText = new System.Windows.Forms.TextBox();
            this.dataTextbox = new System.Windows.Forms.RichTextBox();
            this.sendMessage = new System.Windows.Forms.Button();
            this.attachButton = new System.Windows.Forms.Button();
            this.label4 = new System.Windows.Forms.Label();
            this.ipTextbox = new System.Windows.Forms.TextBox();
            this.portTextbox = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.connectButton = new System.Windows.Forms.Button();
            this.connectErrorLabel = new System.Windows.Forms.Label();
            this.emailErrorLabel = new System.Windows.Forms.Label();
            this.openFileDialog1 = new System.Windows.Forms.OpenFileDialog();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 38);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(23, 13);
            this.label1.TabIndex = 0;
            this.label1.Text = "To:";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 69);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(46, 13);
            this.label2.TabIndex = 1;
            this.label2.Text = "Subject:";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(12, 102);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(53, 13);
            this.label3.TabIndex = 2;
            this.label3.Text = "Message:";
            // 
            // toEmail
            // 
            this.toEmail.Enabled = false;
            this.toEmail.Location = new System.Drawing.Point(67, 38);
            this.toEmail.Name = "toEmail";
            this.toEmail.Size = new System.Drawing.Size(611, 20);
            this.toEmail.TabIndex = 3;
            this.toEmail.TextChanged += new System.EventHandler(this.textBox1_TextChanged);
            // 
            // subjectText
            // 
            this.subjectText.Enabled = false;
            this.subjectText.Location = new System.Drawing.Point(67, 66);
            this.subjectText.Name = "subjectText";
            this.subjectText.Size = new System.Drawing.Size(611, 20);
            this.subjectText.TabIndex = 4;
            // 
            // dataTextbox
            // 
            this.dataTextbox.EnableAutoDragDrop = true;
            this.dataTextbox.Enabled = false;
            this.dataTextbox.Location = new System.Drawing.Point(67, 102);
            this.dataTextbox.Name = "dataTextbox";
            this.dataTextbox.Size = new System.Drawing.Size(611, 96);
            this.dataTextbox.TabIndex = 5;
            this.dataTextbox.Text = "";
            // 
            // sendMessage
            // 
            this.sendMessage.Enabled = false;
            this.sendMessage.Location = new System.Drawing.Point(560, 204);
            this.sendMessage.Name = "sendMessage";
            this.sendMessage.Size = new System.Drawing.Size(118, 23);
            this.sendMessage.TabIndex = 6;
            this.sendMessage.Text = "Send Message";
            this.sendMessage.UseVisualStyleBackColor = true;
            this.sendMessage.Click += new System.EventHandler(this.button1_Click);
            // 
            // attachButton
            // 
            this.attachButton.Enabled = false;
            this.attachButton.Location = new System.Drawing.Point(436, 204);
            this.attachButton.Name = "attachButton";
            this.attachButton.Size = new System.Drawing.Size(118, 23);
            this.attachButton.TabIndex = 7;
            this.attachButton.Text = "Attachment";
            this.attachButton.UseVisualStyleBackColor = true;
            this.attachButton.Click += new System.EventHandler(this.attachButton_Click);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(67, 13);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(19, 13);
            this.label4.TabIndex = 8;
            this.label4.Text = "Ip:";
            // 
            // ipTextbox
            // 
            this.ipTextbox.Location = new System.Drawing.Point(92, 10);
            this.ipTextbox.Name = "ipTextbox";
            this.ipTextbox.Size = new System.Drawing.Size(128, 20);
            this.ipTextbox.TabIndex = 9;
            // 
            // portTextbox
            // 
            this.portTextbox.Location = new System.Drawing.Point(289, 10);
            this.portTextbox.Name = "portTextbox";
            this.portTextbox.Size = new System.Drawing.Size(128, 20);
            this.portTextbox.TabIndex = 11;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(236, 13);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(41, 13);
            this.label5.TabIndex = 10;
            this.label5.Text = "Puerto:";
            this.label5.Click += new System.EventHandler(this.label5_Click);
            // 
            // connectButton
            // 
            this.connectButton.Location = new System.Drawing.Point(423, 10);
            this.connectButton.Name = "connectButton";
            this.connectButton.Size = new System.Drawing.Size(89, 23);
            this.connectButton.TabIndex = 12;
            this.connectButton.Text = "Connect";
            this.connectButton.UseVisualStyleBackColor = true;
            this.connectButton.Click += new System.EventHandler(this.button1_Click_1);
            // 
            // connectErrorLabel
            // 
            this.connectErrorLabel.AutoSize = true;
            this.connectErrorLabel.Location = new System.Drawing.Point(518, 15);
            this.connectErrorLabel.Name = "connectErrorLabel";
            this.connectErrorLabel.Size = new System.Drawing.Size(0, 13);
            this.connectErrorLabel.TabIndex = 13;
            // 
            // emailErrorLabel
            // 
            this.emailErrorLabel.AutoSize = true;
            this.emailErrorLabel.Location = new System.Drawing.Point(86, 230);
            this.emailErrorLabel.Name = "emailErrorLabel";
            this.emailErrorLabel.Size = new System.Drawing.Size(0, 13);
            this.emailErrorLabel.TabIndex = 14;
            // 
            // openFileDialog1
            // 
            this.openFileDialog1.FileName = "openFileDialog1";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(695, 252);
            this.Controls.Add(this.emailErrorLabel);
            this.Controls.Add(this.connectErrorLabel);
            this.Controls.Add(this.connectButton);
            this.Controls.Add(this.portTextbox);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.ipTextbox);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.attachButton);
            this.Controls.Add(this.sendMessage);
            this.Controls.Add(this.dataTextbox);
            this.Controls.Add(this.subjectText);
            this.Controls.Add(this.toEmail);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Name = "Form1";
            this.Text = "Form1";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox toEmail;
        private System.Windows.Forms.TextBox subjectText;
        private System.Windows.Forms.RichTextBox dataTextbox;
        private System.Windows.Forms.Button sendMessage;
        private System.Windows.Forms.Button attachButton;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox ipTextbox;
        private System.Windows.Forms.TextBox portTextbox;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Button connectButton;
        private System.Windows.Forms.Label connectErrorLabel;
        private System.Windows.Forms.Label emailErrorLabel;
        private System.Windows.Forms.OpenFileDialog openFileDialog1;
    }
}

