package com.nkbits.apps.enlist;

import android.app.ProgressDialog;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import org.bouncycastle.util.encoders.Hex;

import java.security.MessageDigest;
import java.util.Objects;

public class LoginActivity extends AppCompatActivity {
    private boolean isRegister = false;
    private EditText emailInput;
    private EditText passwordInput;
    private EditText confirmPasswordInput;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        /*Buttons*/
        final Button registerButton = (Button) findViewById(R.id.register_button);
        final Button loginButton = (Button) findViewById(R.id.login_button);

        /*EditText*/
        emailInput = (EditText) findViewById(R.id.email_input);
        passwordInput = (EditText) findViewById(R.id.password_input);
        confirmPasswordInput = (EditText) findViewById(R.id.confirm_password_input);

        loginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(isRegister) {
                    confirmPasswordInput.setVisibility(View.GONE);
                    registerButton.setText(R.string.Register);
                    loginButton.setText(R.string.Login);
                    isRegister = false;
                }else{
                    if(isValidInput()) {
                        new SendRequest().execute("Login", emailInput.getText().toString(), hashPassword(passwordInput.getText().toString()));
                    }
                }
            }
        });

        registerButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(!isRegister) {
                    confirmPasswordInput.setVisibility(View.VISIBLE);
                    registerButton.setText(R.string.Confirm);
                    loginButton.setText(R.string.Return);
                    isRegister = true;
                }else{
                    if(isValidInput()) {
                        new SendRequest().execute("Register", emailInput.getText().toString(), hashPassword(passwordInput.getText().toString()));
                    }
                }
            }
        });
    }

    private String hashPassword(String password){
        try {
            MessageDigest crypt = MessageDigest.getInstance("SHA-1");
            crypt.reset();
            crypt.update(password.getBytes("utf8"));

            return new String(Hex.encode(crypt.digest()));
        }catch (Exception e){
            return null;
        }
    }

    private boolean isValidInput(){
        if(isRegister){
            return !(Objects.equals(emailInput.getText().toString(), "") ||
                    Objects.equals(passwordInput.getText().toString(), "") ||
                    Objects.equals(confirmPasswordInput.getText().toString(), "") ||
                    !Objects.equals(passwordInput.getText().toString(), confirmPasswordInput.getText().toString()));
        }else{
            return !(Objects.equals(emailInput.getText().toString(), "") ||
                    Objects.equals(passwordInput.getText().toString(), ""));
        }
    }

    class SendRequest extends AsyncTask<String, Void, Boolean> {
        ProgressDialog progressDialog = new ProgressDialog(LoginActivity.this);

        @Override
        protected void onPreExecute(){
            super.onPreExecute();
            progressDialog.setMessage("Loading...");
            progressDialog.setIndeterminate(false);
            progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
            progressDialog.setCancelable(true);
            progressDialog.show();
        }

        @Override
        protected Boolean doInBackground(String... option) {
            String email = option[1];
            String password = option[2];

            switch(option[0]){
                case "Register":
                    if(!UserFacade.create(email, password)){
                        return false;
                    }
                case "Login":
                    Session.user = UserFacade.login(email, password);
                    return Session.user != null;
            }

            return true;
        }

        @Override
        protected void onPostExecute(Boolean success){
            super.onPostExecute(success);
            progressDialog.dismiss();

            if(success){
                Intent myIntent = new Intent(LoginActivity.this, MainActivity.class);
                LoginActivity.this.startActivity(myIntent);
            }else {
                if (isRegister){
                    Snackbar.make(findViewById(R.id.login_layout), "Failed to register!", Snackbar.LENGTH_LONG).setAction("Action", null).show();
                }else{
                    Snackbar.make(findViewById(R.id.login_layout), "Failed to login!", Snackbar.LENGTH_LONG).setAction("Action", null).show();
                }
            }
        }
    }
}
