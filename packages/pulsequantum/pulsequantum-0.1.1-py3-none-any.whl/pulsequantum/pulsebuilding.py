import broadbean as bb
from os import listdir
from os.path import isfile, join
from pathlib import Path
import pathlib
from PyQt5.QtCore import QCoreApplication,Qt
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication, QWidget, QFrame,QMainWindow, QPushButton, QAction, QMessageBox, QLineEdit, QLabel, QSizePolicy
from PyQt5.QtWidgets import QCheckBox,QDialog,QTableWidget,QTableWidgetItem,QVBoxLayout,QHBoxLayout,QComboBox,QGridLayout
from broadbean.plotting import plotter
from pulsequantum.dftable import QTableWidgetDF
from pulsequantum.annotateshape import annotateshape
from pulsequantum.elem_from_plot import elem_on_plot
from pulsequantum.elem_from_plot import elem_from_lists

nchans=2;

ramp = bb.PulseAtoms.ramp # Globally defined ramp, element, and sequence
gelem = bb.Element()
gseq = bb.Sequence()


class Gelem():
    def __init__(self, AWG=None, gelem=None, libpath = 'pulselib/'):
        self.gelem = bb.Element()
        self.table = QTableWidgetDF()
        self.awgclock=1.2e9
        self.libpath = join(pathlib.Path(__file__).parents[0], libpath)
        self.seq_files = [f for f in listdir(self.libpath) if isfile(join(self.libpath, f))]
        self.corrDflag=0
        self.w = None
        self.ch_x = None
        self.ch_y = None
        self.ramp = None

    def generateElement(self):
        # Make element from pulse table
        self.gelem = bb.Element()
        h = int((self.table.columnCount()-2)/3)
        prevlvl = 0
        v = self.table.rowCount()
        for col in range(2,h+2):
            chno=int(self.table.horizontalHeaderItem(col).text()[2]);
            gp = bb.BluePrint()
            gp.setSR(self.awgclock);
            for row in range(v):
                nm=self.table.verticalHeaderItem(row).text();
                dr=(float(self.table.item(row,0).text()))*1e-6;
                rmp=int(self.table.item(row,1).text());
                lvl=(float(self.table.item(row,col).text()))*self.divider_ch[col-2]*1e-3;
                mkr1=int(self.table.item(row,h+2).text());
                mkr2=int(self.table.item(row,h+3).text());
                if rmp==0:
                    gp.insertSegment(row, ramp, (lvl, lvl), name=nm, dur=dr);
                if rmp==1:
                    if row==0:
                        gp.insertSegment(row, ramp, (0, lvl), name=nm, dur=dr);
                    else:
                        gp.insertSegment(row, ramp, (prevlvl, lvl), name=nm, dur=dr);
                if mkr1==1:
                    gp.setSegmentMarker(nm, (0,dr), 1);
                if mkr2==1:
                    gp.setSegmentMarker(nm, (0,dr), 2);
                prevlvl=lvl;
            self.gelem.addBluePrint(chno, gp);
            h=h+2;
        self.gelem.validateDurations();

    def coordinates_from_plot(self, id: int) -> None:
        self.ch_x, self.ch_y, self.ramp = elem_on_plot(id)

    def elem_from_lists_update_table(self,
                                     duration: float = 1e-6, dac_a: float = 0, dac_b: float = 0,
                                     divider_a: float = 1.0, divider_b: float = 1.0,
                                     SR: float = 1e9,
                                     chx: int = 1, chy: int = 2) -> None:    
        self.gelem = elem_from_lists(self.ch_x, self.ch_y, self.ramp, duration, dac_a, dac_b,
                                     divider_a, divider_b, SR, chx, chy)
        self.from_element()

#############################################################################################
# The correction D pulse keeps the centre of gravity of the pulse at the DC value (voltage
# seen by the same when there is no pulsing. Not always used or needed.
#############################################################################################
    def correctionD(self):
        if self.corrDflag==1:
            print("Correction D pulse already exists.")
            return;
        self.corrDflag=1;
        awgclockinus=self.awgclock/1e6;
        tottime=0;
        dpos=1;#position of correction D pulse, hardcoded for now
        self.table.addPulse('corrD',dpos);
        #Set D pulse time to 60% of total pulse cycle time
        for row in range(self.table.rowCount()):
            nm=self.table.verticalHeaderItem(row).text();
            if nm!='corrD':
                tottime=tottime+(float(self.table.item(row,0).text()));
        timeD=round(tottime/1.65*(awgclockinus))/awgclockinus;
        self.table.setItem(dpos,0, QTableWidgetItem("%f"%timeD));
        
        #Correct all voltages in a loop
        for column in range(6):
            tottimevolt=0;
            colnm=self.table.horizontalHeaderItem(column).text();
            for row in range(self.table.rowCount()):
                rownm=self.table.verticalHeaderItem(row).text();
                rmp=int(self.table.item(row,1).text());
                if (rownm!='corrD') and (colnm=='CH1' or colnm=='CH2' or colnm=='CH3' or colnm=='CH4'):
                    if rmp==0:
                        tottimevolt=tottimevolt+((float(self.table.item(row,0).text()))*(float(self.table.item(row,column).text())));
                    if rmp==1:
                        if row==0:
                            tottimevolt=tottimevolt+((float(self.table.item(row,0).text()))*(float(self.table.item(row,column).text()))/2);
                        else:
                            tottimevolt=tottimevolt+((float(self.table.item(row,0).text()))*((float(self.table.item(row,column).text()))+(float(self.table.item(row-1,column).text())))/2);
                voltD=-tottimevolt/timeD;
            if (column!=0) and (column!=1) and (colnm=='CH1' or colnm=='CH2' or colnm=='CH3' or colnm=='CH4'):
                self.table.setItem(dpos,column, QTableWidgetItem("%f"%voltD));
            


############################################################################################    

    def write_element(self, path:str,SR:float = 1e9,SeqAmp:float = 10e-3,SeqOffset:float = 0) -> None:
        if self.gelem.SR == None:
            self.gelem.setSR(SR)
        seqtmp = bb.Sequence()
        seqtmp.addElement(1, self.gelem)
        for ch in self.gelem.channels:
            seqtmp.setChannelAmplitude(ch, SeqAmp)
            seqtmp.setChannelOffset(ch, 0)
        seqtmp.setSR(self.gelem.SR)
        seqtmp.write_to_json(path)

    def saveElement(self,path: str) -> None:
        #self.gelem.write_to_json(path)
        self.write_element(path)
        self.seq_files = [f for f in listdir(self.libpath) if isfile(join(self.libpath, f))]  


    # From Element
    def from_element(self):
         
        elem_description = self.gelem.description
        seg_name = []
        seg_durations = []
        seg_ramp = []
        values = []
        marker1 = []
        marker2 = []
        chan_names = list(elem_description.keys())
        for chan in chan_names:
            ch_values = []
            channels_marker1 = []
            channels_marker2 = []
            marker1_rel = elem_description[chan]['marker1_rel']
            marker2_rel = elem_description[chan]['marker2_rel']
            seg_mar_list = list(elem_description[chan].keys())
            seg_list = [s for s in seg_mar_list if 'segment' in s]
            for i, seg in enumerate(seg_list):
                seg_digt = elem_description[chan][seg]
                tmp_name = seg_digt['name']
                tmp_durations = seg_digt["durations"]
                if tmp_name not in seg_name:
                    seg_name.append(tmp_name)
                    seg_durations.append(tmp_durations)
                    if seg_digt['arguments']['start'] != seg_digt['arguments']['stop']:
                        seg_ramp.append(1)
                    else:
                        seg_ramp.append(0)
                ch_values.append(seg_digt['arguments']['stop'])
                if marker1_rel[i] == (0,0):
                    channels_marker1.append(0)
                else:
                    channels_marker1.append(1)
                    
                if marker2_rel[i] == (0,0):
                    channels_marker2.append(0)
                else:
                    channels_marker2.append(1)             
            values.append(ch_values)
            marker1.append(channels_marker1)
            marker2.append(channels_marker2)
         
        self.nchans = len(values)
        nsegs = len(values[0])


        self.table.setColumnCount((self.nchans*3)+2)
        self.table.setRowCount(nsegs)
        
        #Set horizontal headers
        h=self.nchans+1;
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("Time (us)"));
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem("Ramp? 1=Yes"));
        for i in range(self.nchans): # TODO use the correct channel number as name
            self.table.setHorizontalHeaderItem(i+2, QTableWidgetItem("CH{}".format(chan_names[i])))
            self.table.setHorizontalHeaderItem(h+1, QTableWidgetItem("CH{}M1".format(chan_names[i])))
            self.table.setHorizontalHeaderItem(h+2, QTableWidgetItem("CH{}M2".format(chan_names[i])))
            h=h+2;
        
        #Set vertical headers
        #nlist= seg_name
        for i, name in enumerate(seg_name):
            self.table.setVerticalHeaderItem(i, QTableWidgetItem(name));
            
        
        for seg in range(nsegs):
            duration = str(seg_durations[seg]/1e-6)
            self.table.setItem(seg,0, QTableWidgetItem(duration))
            ramp_yes = str(seg_ramp[seg])
            self.table.setItem(seg,0, QTableWidgetItem(duration))
            self.table.setItem(seg,1, QTableWidgetItem(ramp_yes))
            for ch in range(self.nchans):
               val = str(values[ch][seg]/(self.divider_ch[ch]*1e-3))
               mark1 = str(marker1[ch][seg])
               mark2 = str(marker2[ch][seg])
               self.table.setItem(seg,ch+2, QTableWidgetItem(val))
               self.table.setItem(seg,ch*2+4, QTableWidgetItem(mark1))
               self.table.setItem(seg,ch*2+5, QTableWidgetItem(mark2))

    def loadElement(self, path):
        seq = bb.Sequence.init_from_json(path)
        self.gelem = seq.element(1)
        self.from_element()
        self.generateElement() # TODO IS THIS NEEDED 
        
    def plotElement(self,plotid,gatex,gatey,channelx,channely,dividerx,dividery):
        #if self.w is None:
        #    self.w = PlotWindow(pulse=self.gelem)
        #    self.w.show()
        self.generateElement()
        plotter(self.gelem)
        if plotid != 0:
            annotateshape(plotid,gatex,gatey,self.gelem,channelx,channely,dividerx,dividery)
    

#############################################################################################





      
    