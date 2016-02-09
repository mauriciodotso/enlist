package com.nkbits.apps.enlist;

import android.content.Intent;
import android.os.Bundle;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import org.bouncycastle.util.encoders.Hex;

import java.security.MessageDigest;

public class LoginActivity extends AppCompatActivity {
    private boolean isRegister = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        /*Buttons*/
        final Button registerButton = (Button) findViewById(R.id.register_button);
        final Button loginButton = (Button) findViewById(R.id.login_button);

        /*EditText*/
        final EditText emailInput = (EditText) findViewById(R.id.email_input);
        final EditText passwordInput = (EditText) findViewById(R.id.password_input);
        final EditText confirmPasswordInput = (EditText) findViewById(R.id.confirm_password_input);

        loginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(isRegister) {
                    confirmPasswordInput.setVisibility(View.GONE);
                    registerButton.setText("Register");
                    loginButton.setText("Login");
                    isRegister = false;
                }else{
                    if(isValidInput()) {
                        String email = emailInput.getText().toString();
                        String password = hashPassword(passwordInput.getText().toString());

                        Session.user = UserFacade.login(email, password);

                        if(Session.user == null){
                            Snackbar.make(view, "Failed to login!", Snackbar.LENGTH_LONG)
                                    .setAction("Action", null).show();
                        }else{
                            Intent myIntent = new Intent(LoginActivity.this, MainActivity.class);
                            LoginActivity.this.startActivity(myIntent);
                        }
                    }
                }
            }
        });

        registerButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(!isRegister) {
                    confirmPasswordInput.setVisibility(View.VISIBLE);
                    registerButton.setText("Confirm");
                    loginButton.setText("Return");
                    isRegister = true;
                }else{
                    if(isValidInput()) {
                        String email = emailInput.getText().toString();
                        String password = hashPassword(passwordInput.getText().toString());

                        if(!UserFacade.create(email, password)){
                            Snackbar.make(view, "Failed to register!", Snackbar.LENGTH_LONG)
                                    .setAction("Action", null).show();
                        }

                        Session.user = UserFacade.login(email, password);

                        if(Session.user == null){
                            Snackbar.make(view, "Failed to login!", Snackbar.LENGTH_LONG)
                                    .setAction("Action", null).show();
                        }else{
                            Intent myIntent = new Intent(LoginActivity.this, MainActivity.class);
                            LoginActivity.this.startActivity(myIntent);
                        }
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
        //ToDo: Implement input validation
        if(isRegister){
            return true;
        }else{
            return true;
        }
    }
}
