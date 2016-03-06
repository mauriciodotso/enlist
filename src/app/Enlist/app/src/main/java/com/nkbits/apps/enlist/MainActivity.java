package com.nkbits.apps.enlist;

import android.app.Fragment;
import android.app.FragmentManager;
import android.app.ProgressDialog;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.view.View;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;

public class MainActivity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
            setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
            this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.setDrawerListener(toggle);
        toggle.syncState();

        NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);
    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        SendRequest request = new SendRequest();
        request.execute(item.getItemId());

        return true;
    }

    class SendRequest extends AsyncTask<Integer, Void, Boolean> {
        ProgressDialog progressDialog = new ProgressDialog(MainActivity.this);
        Fragment fragment = null;
        Bundle bundle = new Bundle();
        int id;
        Object data[];

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
        protected Boolean doInBackground(Integer... option) {
            id = option[0];

            switch(id){
                case R.id.nav_my_books:
                    data = BookFacade.getAllByUser(Session.user._id);
                    break;
                case R.id.nav_my_movies:
                    data = MovieFacade.getAllByUser(Session.user._id);
                    break;
                case R.id.nav_search_books:
                    data = BookFacade.getAllNotListed(Session.user._id);
                    break;
                case R.id.nav_search_movies:
                    data = MovieFacade.getAllNotListed(Session.user._id);
                    break;
            }

            return true;
        }

        @Override
        protected void onPostExecute(Boolean success){
            super.onPostExecute(success);
            progressDialog.dismiss();
            bundle.putSerializable(TemplateListView.DATA, data);

            switch(id){
                case R.id.nav_my_books:
                    fragment = new TemplateListView<Book>();
                    bundle.putString(TemplateListView.VIEW, "Book");
                    break;
                case R.id.nav_my_movies:
                    fragment = new TemplateListView<Movie>();
                    bundle.putString(TemplateListView.VIEW, "Movie");
                    break;
                case R.id.nav_search_books:
                    fragment = new SearchListView<Book>();
                    bundle.putString(SearchListView.VIEW, "Book");
                    break;
                case R.id.nav_search_movies:
                    fragment = new SearchListView<Movie>();
                    bundle.putString(SearchListView.VIEW, "Movie");
                    break;
            }

            fragment.setArguments(bundle);

            if (fragment != null) {
                FragmentManager fragmentManager = getFragmentManager();
                fragmentManager.beginTransaction()
                        .replace(R.id.container, fragment).commit();
            }

            DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
            drawer.closeDrawer(GravityCompat.START);
        }
    }
}
