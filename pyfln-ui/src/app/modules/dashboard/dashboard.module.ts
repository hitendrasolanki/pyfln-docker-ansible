import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IndexComponent } from './index/index.component';
import { YamlreadComponent } from './yamlread/yamlread.component';
import { DashboardRoutesModule } from './dashboard-routes.module';
import { FormsModule } from '@angular/forms';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { HttpService } from 'app/services/http.service';

@NgModule({
  imports: [
    CommonModule,
    DashboardRoutesModule,
    FormsModule,
    NgbModule ],
  declarations: [IndexComponent, YamlreadComponent],
  providers: [HttpService]
})
export class DashboardModule { }
