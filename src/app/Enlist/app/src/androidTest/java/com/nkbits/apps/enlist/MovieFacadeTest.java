package com.nkbits.apps.enlist;

import android.test.InstrumentationTestCase;
import com.squareup.okhttp.HttpUrl;
import com.squareup.okhttp.mockwebserver.MockResponse;
import com.squareup.okhttp.mockwebserver.MockWebServer;
import com.squareup.okhttp.mockwebserver.RecordedRequest;

/**
 * <a href="http://d.android.com/tools/testing/testing_android.html">Testing Fundamentals</a>
 */
public class MovieFacadeTest extends InstrumentationTestCase {
    @Override
    protected void setUp() throws Exception {
        super.setUp();
    }

    @Override
    protected void tearDown() throws Exception {
        super.tearDown();
    }

    public void testGet() throws Exception{
        MockWebServer server = new MockWebServer();
        MockResponse response = new MockResponse()
                .addHeader("Content-Type", "application/json; charset=utf-8")
                .addHeader("Cache-Control", "no-cache")
                .setBody("{_id: '507f191e810c19729de860ea', title: 'title', year: 1991}");

        server.enqueue(response);
        server.start();

        HttpUrl baseUrl = server.url("");

        HTTPRequest.setBaseUrl(baseUrl.toString());
        Movie movie = MovieFacade.get("507f191e810c19729de860ea");

        assertEquals("507f191e810c19729de860ea", movie._id);
        assertEquals("title", movie.title);
        assertEquals(1991, movie.year);

        RecordedRequest request = server.takeRequest();
        assertEquals("/movie/get", request.getPath());

        server.shutdown();
    }

    public void testCreate() throws Exception{
        MockWebServer server = new MockWebServer();
        MockResponse response = new MockResponse()
                .addHeader("Content-Type", "application/json; charset=utf-8")
                .addHeader("Cache-Control", "no-cache")
                .setBody("{_id: '507f191e810c19729de860ea'}")
                .setResponseCode(201);

        server.enqueue(response);
        server.start();

        HttpUrl baseUrl = server.url("");

        HTTPRequest.setBaseUrl(baseUrl.toString());
        Movie movie = new Movie("title", 1991);
        String _id = MovieFacade.create(movie, "token");

        assertEquals("507f191e810c19729de860ea",_id);

        RecordedRequest request = server.takeRequest();
        assertEquals("/movie/create", request.getPath());

        server.shutdown();
    }

    public void testUpdate() throws Exception{
        MockWebServer server = new MockWebServer();

        server.enqueue(new MockResponse());
        server.start();

        HttpUrl baseUrl = server.url("");

        HTTPRequest.setBaseUrl(baseUrl.toString());
        Movie movie = new Movie("507f191e810c19729de860ea", "title", 1991);
        boolean status = MovieFacade.update(movie, "token");

        assertEquals(true, status);

        RecordedRequest request = server.takeRequest();
        assertEquals("/movie/update", request.getPath());

        server.shutdown();
    }

    public void testGetAllWithLimit() throws Exception{
        MockWebServer server = new MockWebServer();
        MockResponse response = new MockResponse()
                .addHeader("Content-Type", "application/json; charset=utf-8")
                .addHeader("Cache-Control", "no-cache")
                .setBody("{movies: [{_id: '507f191e810c19729de860ea', title: 'title', year: 1990}," +
                        "{_id: '507f191e810c19729de860eb', title1: 'title', year: 1991}," +
                        "{_id: '507f191e810c19729de860ec', title2: 'title', year: 1992}," +
                        "{_id: '507f191e810c19729de860ed', title3: 'title', year: 1993}," +
                        "{_id: '507f191e810c19729de860ee', title4: 'title', year: 1994}], total: 5, limit: 10}");

        server.enqueue(response);
        server.start();

        HttpUrl baseUrl = server.url("");

        HTTPRequest.setBaseUrl(baseUrl.toString());
        Movie[] movies = MovieFacade.getAll(10, 0);

        assertEquals(5, movies.length);

        RecordedRequest request = server.takeRequest();
        assertEquals("/movie/search", request.getPath());

        server.shutdown();
    }

    public void testSearchByTitleWithLimit() throws Exception{
        MockWebServer server = new MockWebServer();
        MockResponse response = new MockResponse()
                .addHeader("Content-Type", "application/json; charset=utf-8")
                .addHeader("Cache-Control", "no-cache")
                .setBody("{movies: [{_id: '507f191e810c19729de860ea', title: 'title', year: 1990}," +
                        "{_id: '507f191e810c19729de860eb', title1: 'title', year: 1991}," +
                        "{_id: '507f191e810c19729de860ec', title2: 'title', year: 1992}," +
                        "{_id: '507f191e810c19729de860ed', title3: 'title', year: 1993}," +
                        "{_id: '507f191e810c19729de860ee', title4: 'title', year: 1994}], total: 5, limit: 10}");

        server.enqueue(response);
        server.start();

        HttpUrl baseUrl = server.url("");

        HTTPRequest.setBaseUrl(baseUrl.toString());
        Movie[] movies = MovieFacade.searchByTitle("title", 10, 0);

        assertEquals(5, movies.length);

        RecordedRequest request = server.takeRequest();
        assertEquals("/movie/search", request.getPath());

        server.shutdown();
    }
}