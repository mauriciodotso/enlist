package com.nkbits.apps.enlist;

import android.test.InstrumentationTestCase;

import com.squareup.okhttp.HttpUrl;
import com.squareup.okhttp.mockwebserver.MockResponse;
import com.squareup.okhttp.mockwebserver.MockWebServer;
import com.squareup.okhttp.mockwebserver.RecordedRequest;

/**
 * Created by nakayama on 2/6/16.
 */
public class UserFacadeTest extends InstrumentationTestCase {
    @Override
    protected void setUp() throws Exception {
        super.setUp();
    }

    @Override
    protected void tearDown() throws Exception {
        super.tearDown();
    }

    public void testCreate() throws Exception{
        MockWebServer server = new MockWebServer();
        MockResponse response = new MockResponse()
                .addHeader("Content-Type", "application/json; charset=utf-8")
                .addHeader("Cache-Control", "no-cache")
                .setBody("{}")
                .setResponseCode(201);

        server.enqueue(response);
        server.start();

        HttpUrl baseUrl = server.url("");

        HTTPRequest.setBaseUrl(baseUrl.toString());
        boolean success = UserFacade.create("user", "password");

        assertEquals(true, success);

        RecordedRequest request = server.takeRequest();
        assertEquals("/user/create", request.getPath());

        server.shutdown();
    }

    public void testDelete() throws Exception{
        MockWebServer server = new MockWebServer();
        MockResponse response = new MockResponse()
                .addHeader("Content-Type", "application/json; charset=utf-8")
                .addHeader("Cache-Control", "no-cache")
                .setBody("{}")
                .setResponseCode(200);

        server.enqueue(response);
        server.start();

        HttpUrl baseUrl = server.url("");

        HTTPRequest.setBaseUrl(baseUrl.toString());
        boolean success = UserFacade.delete("user", "token");

        assertEquals(true, success);

        RecordedRequest request = server.takeRequest();
        assertEquals("/user/delete", request.getPath());

        server.shutdown();
    }

    public void testUpdate() throws Exception{
        MockWebServer server = new MockWebServer();
        MockResponse response = new MockResponse()
                .addHeader("Content-Type", "application/json; charset=utf-8")
                .addHeader("Cache-Control", "no-cache")
                .setBody("{}")
                .setResponseCode(200);

        server.enqueue(response);
        server.start();

        HttpUrl baseUrl = server.url("");

        HTTPRequest.setBaseUrl(baseUrl.toString());
        boolean success = UserFacade.update("user", "password", "token");

        assertEquals(true, success);

        RecordedRequest request = server.takeRequest();
        assertEquals("/user/update", request.getPath());

        server.shutdown();
    }

    public void testAddBook() throws Exception{
        MockWebServer server = new MockWebServer();
        MockResponse response = new MockResponse()
                .addHeader("Content-Type", "application/json; charset=utf-8")
                .addHeader("Cache-Control", "no-cache")
                .setBody("{}")
                .setResponseCode(200);

        server.enqueue(response);
        server.start();

        HttpUrl baseUrl = server.url("");

        HTTPRequest.setBaseUrl(baseUrl.toString());
        boolean success = UserFacade.addBook("user", "book", "token");

        assertEquals(true, success);

        RecordedRequest request = server.takeRequest();
        assertEquals("/user/addbook", request.getPath());

        server.shutdown();
    }

    public void testUpdateBook() throws Exception{
        MockWebServer server = new MockWebServer();
        MockResponse response = new MockResponse()
                .addHeader("Content-Type", "application/json; charset=utf-8")
                .addHeader("Cache-Control", "no-cache")
                .setBody("{}")
                .setResponseCode(200);

        server.enqueue(response);
        server.start();

        HttpUrl baseUrl = server.url("");

        HTTPRequest.setBaseUrl(baseUrl.toString());
        boolean success = UserFacade.updateBook("user", "book", "token", 1);

        assertEquals(true, success);

        RecordedRequest request = server.takeRequest();
        assertEquals("/user/updatebook", request.getPath());

        server.shutdown();
    }

    public void testAddMovie() throws Exception{
        MockWebServer server = new MockWebServer();
        MockResponse response = new MockResponse()
                .addHeader("Content-Type", "application/json; charset=utf-8")
                .addHeader("Cache-Control", "no-cache")
                .setBody("{}")
                .setResponseCode(200);

        server.enqueue(response);
        server.start();

        HttpUrl baseUrl = server.url("");

        HTTPRequest.setBaseUrl(baseUrl.toString());
        boolean success = UserFacade.addMovie("user", "movie", "token");

        assertEquals(true, success);

        RecordedRequest request = server.takeRequest();
        assertEquals("/user/addmovie", request.getPath());

        server.shutdown();
    }

    public void testUpdateMovie() throws Exception{
        MockWebServer server = new MockWebServer();
        MockResponse response = new MockResponse()
                .addHeader("Content-Type", "application/json; charset=utf-8")
                .addHeader("Cache-Control", "no-cache")
                .setBody("{}")
                .setResponseCode(200);

        server.enqueue(response);
        server.start();

        HttpUrl baseUrl = server.url("");

        HTTPRequest.setBaseUrl(baseUrl.toString());
        boolean success = UserFacade.updateMovie("user", "book", "token", 1);

        assertEquals(true, success);

        RecordedRequest request = server.takeRequest();
        assertEquals("/user/updatemovie", request.getPath());

        server.shutdown();
    }

    public void testLogin() throws Exception{
        MockWebServer server = new MockWebServer();
        MockResponse response = new MockResponse()
                .addHeader("Content-Type", "application/json; charset=utf-8")
                .addHeader("Cache-Control", "no-cache")
                .setBody("{'token': 'token'}")
                .setResponseCode(200);

        server.enqueue(response);
        server.start();

        HttpUrl baseUrl = server.url("");

        HTTPRequest.setBaseUrl(baseUrl.toString());
        User user = UserFacade.login("user", "password");

        assertEquals(user.token, "token");
        assertEquals(user._id, "user");

        RecordedRequest request = server.takeRequest();
        assertEquals("/login", request.getPath());

        server.shutdown();
    }

    public void testLogout() throws Exception{
        MockWebServer server = new MockWebServer();
        MockResponse response = new MockResponse()
                .addHeader("Content-Type", "application/json; charset=utf-8")
                .addHeader("Cache-Control", "no-cache")
                .setBody("{}")
                .setResponseCode(200);

        server.enqueue(response);
        server.start();

        HttpUrl baseUrl = server.url("");

        HTTPRequest.setBaseUrl(baseUrl.toString());
        boolean success = UserFacade.logout("token");

        assertEquals(true, success);

        RecordedRequest request = server.takeRequest();
        assertEquals("/logout", request.getPath());

        server.shutdown();
    }
}
