import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { PredictComponent } from './pages/predict/predict.component';
import { VisualizationComponent } from './pages/visualization/visualization.component';
import { ModelInfoComponent } from './pages/model-info/model-info.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'predict', component: PredictComponent },
  { path: 'visualization', component: VisualizationComponent },
  { path: 'model', component: ModelInfoComponent },
  { path: '**', redirectTo: '' }
];
