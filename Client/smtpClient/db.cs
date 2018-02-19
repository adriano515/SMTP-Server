using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using MySql.Data.MySqlClient;
using System.Data;
using System.Windows.Forms;
using System.Drawing;

namespace smtpClient
{
    class db
    {
        String MyConnectionString = "Server=localhost;Database=smtp;Uid=root;Pwd=;";
        public bool insert(String id, String from, String to, String subject, String text, String user) {
            MySqlConnection connection = new MySqlConnection(MyConnectionString);
            MySqlCommand cmd;
            connection.Open();
            try
            {
                cmd = connection.CreateCommand();
                cmd.CommandText = "insert into emails(id,from,to,subject,text,user) values("+ id + ","+ from + ","+ to + ","+ subject + ","+ text + ","+ user + ",)";
                cmd.ExecuteNonQuery();
                return true;
            }
            catch (Exception e) {
                return false;
            }
        }

        public DataTable fillTable(String user) {
            MySqlConnection connection = new MySqlConnection(MyConnectionString);
            MySqlCommand cmd;
            connection.Open();
            try {
                cmd = connection.CreateCommand();
                String sqlSelectAll = "SELECT subject,id FROM `emails` WHERE `user` = '"+user+"'";
                MySqlDataAdapter adap = new MySqlDataAdapter(sqlSelectAll, connection);
                DataSet DS = new DataSet();
                adap.Fill(DS);
                return DS.Tables[0];

            }
            catch (Exception e) {
                throw;
            }
        }
        public List<String> getEmailData(String id)
        {
            string query = "Select `from`,`subject`,`text` from emails where `id`="+id+"";
            List<String> list = new List<String>();
            MySqlConnection connection = new MySqlConnection(MyConnectionString);
            connection.Open();
            try {
                MySqlCommand cmd = new MySqlCommand(query, connection);
                MySqlDataReader dataReader = cmd.ExecuteReader();
                dataReader.Read();
                list.Add(dataReader["from"] + "");
                list.Add(dataReader["subject"] + "");
                list.Add(dataReader["text"] + "");
                dataReader.Close();
                connection.Close();
                return list;
            }
            catch(Exception e) {
                connection.Close();
                throw;
            }
        }
    }
}
