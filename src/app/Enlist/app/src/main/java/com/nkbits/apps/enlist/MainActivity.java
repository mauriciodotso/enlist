package com.nkbits.apps.enlist;

import android.app.Fragment;
import android.app.FragmentManager;
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

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();
        Fragment fragment = null;
        Bundle bundle = new Bundle();

        if (id == R.id.nav_my_books) {
            Book book_data[] = new Book[]
                    {
                            new Book("Cloudy", 1, 1900),
                            new Book("Showers", 2, 1910),
                            new Book("Snow", 3, 1920),
                            new Book("Storm", 4, 1930),
                            new Book("Sunny", 5, 1940)
                    };

            fragment = new TemplateListView<Book>();
            bundle.putSerializable(TemplateListView.DATA, book_data);
            bundle.putString(TemplateListView.VIEW, "Book");
            fragment.setArguments(bundle);
        } else if (id == R.id.nav_my_movies) {
            Movie movie_data[] = new Movie[]
                    {
                            new Movie("Cloudy", 1900),
                            new Movie("Showers", 1910),
                            new Movie("Snow", 1920),
                            new Movie("Storm", 1930),
                            new Movie("Sunny", 1940)
                    };

            fragment = new TemplateListView<Movie>();
            bundle.putSerializable(TemplateListView.DATA, movie_data);
            bundle.putString(TemplateListView.VIEW, "Movie");
            fragment.setArguments(bundle);
        } else if (id == R.id.nav_search_books) {
            Book book_data[] = new Book[]
                    {
                            new Book("Cloudy", 1, 1900),
                            new Book("Showers", 2, 1910),
                            new Book("Snow", 3, 1920),
                            new Book("Storm", 4, 1930),
                            new Book("Sunny", 5, 1940)
                    };

            fragment = new SearchListView<>();
            bundle.putSerializable(SearchListView.DATA, book_data);
            bundle.putString(SearchListView.VIEW, "Book");
            fragment.setArguments(bundle);
        } else if (id == R.id.nav_search_movies) {
            Movie movie_data[] = new Movie[]
                    {
                            new Movie("Cloudy", 1900),
                            new Movie("Showers", 1910),
                            new Movie("Snow", 1920),
                            new Movie("Storm", 1930),
                            new Movie("Sunny", 1940)
                    };

            fragment = new SearchListView<Movie>();
            bundle.putSerializable(SearchListView.DATA, movie_data);
            bundle.putString(SearchListView.VIEW, "Movie");
            fragment.setArguments(bundle);
        }

        if (fragment != null) {
            FragmentManager fragmentManager = getFragmentManager();
            fragmentManager.beginTransaction()
                    .replace(R.id.container, fragment).commit();
        }

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }
}
