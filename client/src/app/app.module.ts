import { NgModule } from '@angular/core';

import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http'; // Import HttpClientModule
import { AppComponent } from './app.component';
import { APIService } from './api.service';

@NgModule({
  declarations: [AppComponent],
  imports: [BrowserModule, FormsModule, HttpClientModule], // Include HttpClientModule in imports
  providers: [APIService], // Add APIService to the providers array
  bootstrap: [AppComponent]
})
export class AppModule {}
