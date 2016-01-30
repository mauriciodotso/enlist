package com.nkbits.apps.enlist;

import com.squareup.okhttp.HttpUrl;
import com.squareup.okhttp.mockwebserver.MockResponse;
import com.squareup.okhttp.mockwebserver.MockWebServer;
import com.squareup.okhttp.mockwebserver.RecordedRequest;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * To work on unit tests, switch the Test Artifact in the Build Variants view.
 */
public class BookFacadeUnitTest {
    @Test
    public void testGet() throws Exception{
        MockWebServer server = new MockWebServer();
        MockResponse response = new MockResponse()
                .addHeader("Content-Type", "application/json; charset=utf-8")
                .addHeader("Cache-Control", "no-cache")
                .setBody("{_id: '507f191e810c19729de860ea', title: 'title', edition: 1, year: 1991}");

        server.enqueue(response);
        server.start();

        HttpUrl baseUrl = server.url("");

        HTTPRequest.setBaseUrl(baseUrl.toString());
        Book book = BookFacade.get("507f191e810c19729de860ea");

        // Optional: confirm that your app made the HTTP requests you were expecting.
        RecordedRequest request1 = server.takeRequest();
        assertEquals("/v1/chat/messages/", request1.getPath());
        assertNotNull(request1.getHeader("Authorization"));

        RecordedRequest request2 = server.takeRequest();
        assertEquals("/v1/chat/messages/2", request2.getPath());

        RecordedRequest request3 = server.takeRequest();
        assertEquals("/v1/chat/messages/3", request3.getPath());

        // Shut down the server. Instances cannot be reused.
        server.shutdown();
    }

    @Test
    public void testCreate() throws Exception{
    }

    @Test
    public void testUpdate() throws Exception{
    }

    @Test
    public void testGetAllWithLimit() throws Exception{
    }

    @Test
    public void testGetAll() throws Exception{
    }

    @Test
    public void testSearchByTitleWithLimit() throws Exception{
    }

    @Test
    public void testSearchByTitle() throws Exception{
    }
}