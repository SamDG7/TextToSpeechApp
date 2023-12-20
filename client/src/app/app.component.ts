// Import necessary modules
import { Component} from '@angular/core';
import { NgModel } from '@angular/forms';
// Import your service
import { APIService } from './api.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  providers: [NgModel]
})
export class AppComponent {
  voices = ["Matthew", "Joanna", "Ivy", "Justin"];
  selectedVoice = "Matthew";

  constructor(private api: APIService) {}

  playAudio(url: any) {
    let audio = new Audio();
    audio.src = url;
    audio.load();
    audio.play();
  }

  speakNow(input: any, selectedVoice: any) {
    console.log(input, selectedVoice);
    let data = {
      text: input,
      voice: selectedVoice
    };
    this.api.speak(data).subscribe((result: any) => {
      console.log(result, result.signed_url);
      this.playAudio(result.signed_url);
    });
  }
  
}
