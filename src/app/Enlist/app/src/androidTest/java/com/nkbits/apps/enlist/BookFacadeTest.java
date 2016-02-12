package com.nkbits.apps.enlist;

import android.test.InstrumentationTestCase;
import com.squareup.okhttp.HttpUrl;
import com.squareup.okhttp.mockwebserver.MockResponse;
import com.squareup.okhttp.mockwebserver.MockWebServer;
import com.squareup.okhttp.mockwebserver.RecordedRequest;

/**
 * <a href="http://d.android.com/tools/testing/testing_android.html">Testing Fundamentals</a>
 */
public class BookFacadeTest extends InstrumentationTestCase {
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
                .setBody("{_id: '507f191e810c19729de860ea', title: 'title', edition: 1, year: 1991}");

        server.enqueue(response);
        server.start();

        HttpUrl baseUrl = server.url("");

        HTTPRequest.setBaseUrl(baseUrl.toString());
        Book book = BookFacade.get("507f191e810c19729de860ea");

        assertEquals("507f191e810c19729de860ea", book._id);
        assertEquals("title", book.title);
        assertEquals(1, book.edition);
        assertEquals(1991, book.year);

        RecordedRequest request = server.takeRequest();
        assertEquals("/book/get", request.getPath());

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
        Book book = new Book("title", 1, 1991);
        String _id = BookFacade.create(book, "token");

        assertEquals("507f191e810c19729de860ea",_id);

        RecordedRequest request = server.takeRequest();
        assertEquals("/book/create", request.getPath());

        server.shutdown();
    }

    public void testUpdate() throws Exception{
        MockWebServer server = new MockWebServer();

        server.enqueue(new MockResponse());
        server.start();

        HttpUrl baseUrl = server.url("");

        HTTPRequest.setBaseUrl(baseUrl.toString());
        Book book = new Book("507f191e810c19729de860ea", "title", 1, 1991);
        boolean status = BookFacade.update(book, "token");

        assertEquals(true, status);

        RecordedRequest request = server.takeRequest();
        assertEquals("/book/update", request.getPath());

        server.shutdown();
    }

    public void testGetAllWithLimit() throws Exception{
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
        Book[] books = BookFacade.getAll(10, 0);

        assertEquals(5, books.length);

        RecordedRequest request = server.takeRequest();
        assertEquals("/book/search", request.getPath());

        server.shutdown();
    }

    public void testSearchByTitleWithLimit() throws Exception{
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
        Book[] books = BookFacade.searchByTitle("title", 10, 0);

        assertEquals(5, books.length);

        RecordedRequest request = server.takeRequest();
        assertEquals("/book/search", request.getPath());

        server.shutdown();
    }

    public void testGetAllByUser() throws Exception{
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
        Book[] books = BookFacade.getAllByUser("user", 10, 0);

        assertEquals(5, books.length);

        RecordedRequest request = server.takeRequest();
        assertEquals("/book/search", request.getPath());

        server.shutdown();
    }
}