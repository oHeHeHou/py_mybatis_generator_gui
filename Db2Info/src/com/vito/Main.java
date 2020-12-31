package com.vito;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

public class Main {

    public static String db = null;
    public static String user = null;
    public static String password = null;
    public static Connection mConnection = null;
    public static boolean isTest = false;
    public static Statement mStatement;


    public static void main(String[] args) {

        for (String arg : args) {
            if (arg.startsWith("-c")) {
                db = arg.substring(2);
            }
            if (arg.startsWith("-u")) {
                user = arg.substring(2);
            }
            if (arg.startsWith("-p")) {
                password = arg.substring(2);
            }
            if (arg.equalsIgnoreCase("-test")) {
                isTest = true;
            }
            if (arg.equalsIgnoreCase("-list")) {
                isTest = false;
            }
        }

        if (isTest) {
            try {
                Class.forName("com.ibm.db2.jcc.DB2Driver");
                mConnection = DriverManager.getConnection(db, user, password);
                mConnection.close();
                System.out.print("yes");
            } catch (ClassNotFoundException | SQLException e) {
                System.out.print("no");
            }
        } else {
            String sql = "select TABNAME from SYSCAT.TABLES where TABSCHEMA=(select current schema from SYSIBM.SYSDUMMY1)";
            try {
                Class.forName("com.ibm.db2.jcc.DB2Driver");
                mConnection = DriverManager.getConnection(db, user, password);
                mStatement = mConnection.createStatement();
                ResultSet resultSet = mStatement.executeQuery(sql);
                List<String> tableNames = new ArrayList<>();
                while (resultSet.next()) {
                    tableNames.add(resultSet.getString(1));
                }
                resultSet.close();
                mStatement.close();
                mConnection.close();
                System.out.print(tableNames);
            } catch (ClassNotFoundException | SQLException e) {
                e.printStackTrace();
            }
        }
    }
}
