package com.nkbits.apps.enlist;

import android.support.test.espresso.matcher.ViewMatchers;
import android.support.test.rule.ActivityTestRule;

import com.squareup.okhttp.HttpUrl;
import com.squareup.okhttp.mockwebserver.MockResponse;
import com.squareup.okhttp.mockwebserver.MockWebServer;

import static android.support.test.espresso.Espresso.onView;
import static android.support.test.espresso.action.ViewActions.click;
import static android.support.test.espresso.action.ViewActions.closeSoftKeyboard;
import static android.support.test.espresso.action.ViewActions.typeText;
import static android.support.test.espresso.assertion.ViewAssertions.doesNotExist;
import static android.support.test.espresso.assertion.ViewAssertions.matches;
import static android.support.test.espresso.matcher.ViewMatchers.isDisplayed;
import static android.support.test.espresso.matcher.ViewMatchers.withEffectiveVisibility;
import static android.support.test.espresso.matcher.ViewMatchers.withId;

import org.junit.Rule;
import org.junit.Test;


/**
 * Created by nakayama on 2/19/16.
 */


public class LoginActivityTest {
    private String userEmail = "test@test.com";
    private String userPassword = "123456";

    @Rule
    public ActivityTestRule<LoginActivity> mActivityRule = new ActivityTestRule<>(
            LoginActivity.class);


    @Test
    public void testStartRegistration() throws Exception{
        // Press the register button
        onView(withId(R.id.register_button)).perform(click());

        // Check that the confirm password appeared.
        onView(withId(R.id.confirm_password_input))
                .check(matches(isDisplayed()));

        // Press the return button
        onView(withId(R.id.login_button)).perform(click());

        // Check that the confirm password disappeared.
        onView(withId(R.id.confirm_password_input))
                .check(matches(withEffectiveVisibility(ViewMatchers.Visibility.GONE)));
    }

    @Test
    public void testRegister() throws Exception{
        MockWebServer server = new MockWebServer();
        MockResponse registerResponse = new MockResponse()
                .addHeader("Content-Type", "application/json; charset=utf-8")
                .addHeader("Cache-Control", "no-cache")
                .setBody("{}")
                .setResponseCode(201);

        MockResponse loginResponse = new MockResponse()
                .addHeader("Content-Type", "application/json; charset=utf-8")
                .addHeader("Cache-Control", "no-cache")
                .setBody("{'token': 'token'}")
                .setResponseCode(200);

        server.enqueue(registerResponse);
        server.enqueue(loginResponse);
        server.start();

        HttpUrl baseUrl = server.url("");

        HTTPRequest.setBaseUrl(baseUrl.toString());

        // Press the register button
        onView(withId(R.id.register_button)).perform(click());

        //Type registration inputs
        onView(withId(R.id.email_input))
                .perform(typeText(userEmail), closeSoftKeyboard());

        onView(withId(R.id.password_input))
                .perform(typeText(userPassword), closeSoftKeyboard());

        onView(withId(R.id.confirm_password_input))
                .perform(typeText(userPassword), closeSoftKeyboard());

        // Register
        onView(withId(R.id.register_button)).perform(click());

        // Check that LoginActivity has been replaced.
        onView(withId(R.id.login_layout))
                .check(doesNotExist());

        // Check that MainActivity is displayed.
        onView(withId(R.id.drawer_layout))
                .check(matches(isDisplayed()));

        server.shutdown();
    }

    @Test
    public void testLogin() throws Exception{
        MockWebServer server = new MockWebServer();

        MockResponse loginResponse = new MockResponse()
                .addHeader("Content-Type", "application/json; charset=utf-8")
                .addHeader("Cache-Control", "no-cache")
                .setBody("{'token': 'token'}")
                .setResponseCode(200);

        server.enqueue(loginResponse);
        server.start();

        HttpUrl baseUrl = server.url("");

        HTTPRequest.setBaseUrl(baseUrl.toString());

        //Type registration inputs
        onView(withId(R.id.email_input))
                .perform(typeText(userEmail), closeSoftKeyboard());

        onView(withId(R.id.password_input))
                .perform(typeText(userPassword), closeSoftKeyboard());

        // Register
        onView(withId(R.id.login_button)).perform(click());

        // Check that LoginActivity has been replaced.
        onView(withId(R.id.login_layout))
                .check(doesNotExist());

        // Check that MainActivity is displayed.
        onView(withId(R.id.drawer_layout))
                .check(matches(isDisplayed()));

        server.shutdown();
    }
}
