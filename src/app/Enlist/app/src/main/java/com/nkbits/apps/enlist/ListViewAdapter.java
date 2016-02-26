package com.nkbits.apps.enlist;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Context;
import android.os.AsyncTask;
import android.support.design.widget.Snackbar;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by nakayama on 1/23/16.
 */
public class ListViewAdapter<T> extends ArrayAdapter<T>{
    Context context;
    int layoutResourceId;
    ArrayList<T> data = null;
    String dataId;
    int status;
    View view;

    public ListViewAdapter(Context context, int layoutResourceId, ArrayList<T> data) {
        super(context, layoutResourceId, data);
        this.layoutResourceId = layoutResourceId;
        this.context = context;
        this.data = data;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        if(convertView == null)
        {
            LayoutInflater inflater = ((Activity)context).getLayoutInflater();
            convertView = inflater.inflate(layoutResourceId, parent, false);
        }

        view = convertView;

        TextView titleText = (TextView) convertView.findViewById(R.id.title_text);
        TextView yearText = (TextView) convertView.findViewById(R.id.year_text);
        Button actionButton = (Button) convertView.findViewById(R.id.action_button);

        switch (layoutResourceId){
            case R.layout.book_view:
                final Book book = (Book)getItem(position);
                TextView editionText = (TextView) convertView.findViewById(R.id.edition_text);
                titleText.setText(book.title);
                yearText.setText(Integer.toString(book.year));
                editionText.setText(Integer.toString(book.edition));
                this.dataId = book._id;
                this.status = book.status;

                if(this.status == 0){
                    actionButton.setText("Read");
                }else if(this.status == 1){
                    actionButton.setVisibility(View.GONE);
                }

                actionButton.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        SendRequest request = new SendRequest();
                        request.execute("Book", book._id);
                    }
                });
                break;
            case R.layout.movie_view:
                final Movie movie = (Movie)getItem(position);
                titleText.setText(movie.title);
                yearText.setText(Integer.toString(movie.year));
                this.dataId = movie._id;
                this.status = movie.status;

                if(this.status == 0){
                    actionButton.setText("Viewed");
                }else if(this.status == 1){
                    actionButton.setVisibility(View.GONE);
                }

                actionButton.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        SendRequest request = new SendRequest();
                        request.execute("Movie", movie._id);
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
                    if(status == -1) {
                        UserFacade.addBook(Session.user._id, option[1], Session.user.token);
                    }else{
                        UserFacade.updateBook(Session.user._id, option[1], Session.user.token, 1);
                    }
                    break;
                case "Movie":
                    if(status == -1) {
                        UserFacade.addMovie(Session.user._id, option[1], Session.user.token);
                    }else{
                        UserFacade.updateMovie(Session.user._id, option[1], Session.user.token, 1);
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
                if(status == 0) {
//                    Snackbar.make(view.findViewById(R.id.list_view), "Item added to your list!", Snackbar.LENGTH_LONG).setAction("Action", null).show();
                }else{
//                    Snackbar.make(view.findViewById(R.id.list_view), "Item updated!", Snackbar.LENGTH_LONG).setAction("Action", null).show();
                }
            }else {
                if(status == 0) {
//                    Snackbar.make(view.findViewById(R.id.list_view), "Failed to add to your list!", Snackbar.LENGTH_LONG).setAction("Action", null).show();
                }else {
//                    Snackbar.make(view.findViewById(R.id.list_view), "Failed to update!", Snackbar.LENGTH_LONG).setAction("Action", null).show();
                }
            }
        }
    }
}
