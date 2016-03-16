package com.nkbits.apps.enlist;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Context;
import android.os.AsyncTask;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.Objects;

/**
 * Created by nakayama on 1/23/16.
 */
public class ListViewAdapter<T> extends ArrayAdapter<T>{
    Context context;
    int layoutResourceId;
    ArrayList<T> data = null;
    View view;
    int lastClickedPosition;

    public ListViewAdapter(Context context, int layoutResourceId, ArrayList<T> data) {
        super(context, layoutResourceId, data);
        this.layoutResourceId = layoutResourceId;
        this.context = context;
        this.data = data;
    }

    @Override
    public View getView(final int position, View convertView, ViewGroup parent) {
        if(convertView == null)
        {
            LayoutInflater inflater = ((Activity)context).getLayoutInflater();
            convertView = inflater.inflate(layoutResourceId, parent, false);
        }

        view = convertView;

        TextView titleText = (TextView) convertView.findViewById(R.id.title_text);
        TextView yearText = (TextView) convertView.findViewById(R.id.year_text);
        Button actionButton = (Button) convertView.findViewById(R.id.action_button);
        Button deleteButton = (Button) convertView.findViewById(R.id.delete_button);
        final String action;

        switch (layoutResourceId){
            case R.layout.book_view:
                final Book book = (Book)getItem(position);
                TextView editionText = (TextView) convertView.findViewById(R.id.edition_text);
                titleText.setText(book.title);
                yearText.setText(Integer.toString(book.year));
                editionText.setText(Integer.toString(book.edition));

                if(book.status == 0){
                    actionButton.setText("Read");
                    action = "markRead";
                }else if(book.status == 1){
                    actionButton.setText("Unread");
                    action = "markUnread";
                }else{
                    action = "add";
                    deleteButton.setVisibility(View.GONE);
                }

                actionButton.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        lastClickedPosition = position;
                        SendRequest request = new SendRequest();
                        request.execute("Book", book._id, action);
                    }
                });

                deleteButton.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        lastClickedPosition = position;
                        SendRequest request = new SendRequest();
                        request.execute("Book", book._id, "delete");
                    }
                });
                break;
            case R.layout.movie_view:
                final Movie movie = (Movie)getItem(position);
                titleText.setText(movie.title);
                yearText.setText(Integer.toString(movie.year));

                if(movie.status == 0){
                    actionButton.setText("Viewed");
                    action = "markSeen";
                }else if(movie.status == 1){
                    actionButton.setText("Unmark");
                    action = "markUnseen";
                }else{
                    action = "add";
                    deleteButton.setVisibility(View.GONE);
                }

                actionButton.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        lastClickedPosition = position;
                        SendRequest request = new SendRequest();
                        request.execute("Movie", movie._id, action);
                    }
                });

                deleteButton.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        lastClickedPosition = position;
                        SendRequest request = new SendRequest();
                        request.execute("Movie", movie._id, "delete");
                    }
                });
                break;
        }

        return convertView;
    }

    public void clear(){
        this.data.clear();
    }

    public void update(ArrayList<T> data){
        this.data = data;
        this.notifyDataSetChanged();
    }

    class SendRequest extends AsyncTask<String, Void, Boolean> {
        ProgressDialog progressDialog = new ProgressDialog(context);
        int status = 0;

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
        protected Boolean doInBackground(String... option) {
            switch(option[0]){
                case "Book":
                    if(Objects.equals(option[2], "add")) {
                        UserFacade.addBook(Session.user._id, option[1], Session.user.token);
                        status = -1;
                    }else if(Objects.equals(option[2], "markRead")){
                        UserFacade.updateBook(Session.user._id, option[1], Session.user.token, 1);
                        status = 1;
                    }else if(Objects.equals(option[2], "markUnread")){
                        UserFacade.updateBook(Session.user._id, option[1], Session.user.token, 0);
                    }else if(Objects.equals(option[2], "delete")){
                        UserFacade.deleteBook(Session.user._id, option[1], Session.user.token);
                    }
                    break;
                case "Movie":
                    if(Objects.equals(option[2], "add")) {
                        UserFacade.addMovie(Session.user._id, option[1], Session.user.token);
                        status = -1;
                    }else if(Objects.equals(option[2], "markSeen")){
                        UserFacade.updateMovie(Session.user._id, option[1], Session.user.token, 1);
                        status = 1;
                    }else if(Objects.equals(option[2], "markUnseen")){
                        UserFacade.updateMovie(Session.user._id, option[1], Session.user.token, 0);
                    }else if(Objects.equals(option[2], "delete")){
                        UserFacade.deleteMovie(Session.user._id, option[1], Session.user.token);
                    }
                    break;
            }

            return true;
        }

        @Override
        protected void onPostExecute(Boolean success){
            super.onPostExecute(success);
            progressDialog.dismiss();

            if(success){
                if(status == -1){
                    data.remove(lastClickedPosition);
                }else {
                    switch (layoutResourceId) {
                        case R.layout.book_view:
                            ((Book) (data.get(lastClickedPosition))).status = status;
                            break;
                        case R.layout.movie_view:
                            ((Movie) (data.get(lastClickedPosition))).status = status;
                            break;
                    }
                }

                notifyDataSetChanged();
                //ToDo: Update View
            }else {
                //ToDo: Display Error Message
            }
        }
    }
}
