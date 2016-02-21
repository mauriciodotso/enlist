package com.nkbits.apps.enlist;

import android.support.design.internal.NavigationMenuItemView;
import android.support.design.widget.NavigationView;
import android.support.test.rule.ActivityTestRule;
import android.view.MenuItem;
import android.view.View;

import com.squareup.okhttp.HttpUrl;
import com.squareup.okhttp.mockwebserver.MockResponse;
import com.squareup.okhttp.mockwebserver.MockWebServer;

import org.hamcrest.Matchers;
import org.junit.Rule;
import org.junit.Test;

import static android.support.test.espresso.Espresso.onData;
import static android.support.test.espresso.Espresso.onView;
import static android.support.test.espresso.action.ViewActions.click;
import static android.support.test.espresso.assertion.ViewAssertions.matches;
import static android.support.test.espresso.contrib.DrawerActions.openDrawer;
import static android.support.test.espresso.contrib.DrawerMatchers.isOpen;
import static android.support.test.espresso.matcher.PreferenceMatchers.withTitle;
import static android.support.test.espresso.matcher.ViewMatchers.hasSibling;
import static android.support.test.espresso.matcher.ViewMatchers.withId;
import static android.support.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.instanceOf;
import static org.hamcrest.Matchers.is;

/**
 * Created by nakayama on 2/21/16.
 */
public class MainActivityTest {

    @Rule
    public ActivityTestRule<MainActivity> mActivityRule = new ActivityTestRule<>(
            MainActivity.class);


    @Test
    public void testListAllBooks() throws Exception{
        MockWebServer server = new MockWebServer();
        MockResponse response = new MockResponse()
                .addHeader("Content-Type", "application/json; charset=utf-8")
                .addHeader("Cache-Control", "no-cache")
                .setBody("{books: [{_id: '507f191e810c19729de860ea', title: 'title', edition: 0, year: 1990}," +
                        "{_id: '507f191e810c19729de860eb', title1: 'title', edition: 1, year: 1991}," +
                        "{_id: '507f191e810c19729de860ec', title2: 'title', edition: 2, year: 1992}," +
                        "{_id: '507f191e810c19729de860ed', title3: 'title', edition: 3, year: 1993}," +
                        "{_id: '507f191e810c19729de860ee', title4: 'title', edition: 4, year: 1994}], total: 5, limit: 10}");

        server.enqueue(response);
        server.start();

        HttpUrl baseUrl = server.url("");

        HTTPRequest.setBaseUrl(baseUrl.toString());

        Session.user = new User("username", "Token");

        openDrawer(R.id.drawer_layout);

        //Tests if Drawer is open
        onView(withId(R.id.drawer_layout)).check(matches(isOpen()));

        onView(withText(R.string.my_books)).perform(click());
    }
}
