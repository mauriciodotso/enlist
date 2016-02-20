package com.nkbits.apps.enlist;

import android.support.test.rule.ActivityTestRule;
import android.support.test.runner.AndroidJUnit4;
import android.test.suitebuilder.annotation.LargeTest;

import static android.support.test.espresso.Espresso.onView;
import static android.support.test.espresso.action.ViewActions.click;
import static android.support.test.espresso.assertion.ViewAssertions.matches;
import static android.support.test.espresso.matcher.ViewMatchers.isDisplayed;
import static android.support.test.espresso.matcher.ViewMatchers.withId;

import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;


/**
 * Created by nakayama on 2/19/16.
 */


public class LoginActivityTest {
    private String userEmail;

    @Rule
    public ActivityTestRule<LoginActivity> mActivityRule = new ActivityTestRule<>(
            LoginActivity.class);


    @Test
    public void testStartRegistration() throws Exception{
        // Press the register button
        onView(withId(R.id.register_button)).perform(click());

        // Check that the text was changed.
        onView(withId(R.id.confirm_password_input))
                .check(matches(isDisplayed()));
    }
}
