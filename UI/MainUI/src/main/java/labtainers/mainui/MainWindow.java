/*
This software was created by United States Government employees at 
The Center for Cybersecurity and Cyber Operations (C3O) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
*/
package labtainers.mainui;

import java.awt.Component;
import java.awt.Dimension;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.File;
import java.nio.file.Files;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FilenameFilter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.InputStream;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Properties;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JFileChooser;
import javax.swing.JScrollBar;
import java.util.function.Consumer;
import java.util.Arrays;
import java.util.ArrayList;
import java.lang.ClassLoader;
import java.lang.Thread;
import java.nio.charset.StandardCharsets;
import javax.swing.ImageIcon;
import javax.imageio.ImageIO;
import javax.swing.JDialog;
import javax.swing.JOptionPane;
import java.util.concurrent.Executors;
import java.util.Collections;

import labtainers.mainui.LabData.ContainerData;
import labtainers.mainui.LabData.NetworkData;
import labtainers.goalsui.GoalsUI;
import labtainers.resultsui.ResultsData;
import labtainers.resultsui.ResultsUI;
import labtainers.paramsui.ParamsData;
import labtainers.paramsui.ParamsUI;


/**
 *
 * @author Daniel Liao
 */
public class MainWindow extends javax.swing.JFrame {
    private LabData labDataCurrent;
    private String labtainerPath;
    private File labsPath;
    private String labName;
    private File currentLab=null;
    private final File iniFile;
    private final Properties prefProperties;
    private String[] bases;
    private String textEditorPref;
    
    SimpleDateFormat formatter;
    Date date;
            
    private ResultsUI resultsUI;
    private GoalsUI goalsUI;
    private ParamsUI paramsUI;
    private boolean resultsOpened;
    private boolean goalsOpened;
    private boolean paramsOpened;
      
    public MainWindow() throws IOException {
        initComponents();
        setMnemonics();
        
        containerScrollPaneBar = ContainerScrollPane.getVerticalScrollBar();
        networkScrollPaneBar = NetworkScrollPane.getVerticalScrollBar();
        LabExistLabel.setVisible(false);
        
        iniFile = new File(System.getenv("HOME")+File.separator+".local/share/labtainers/UI.ini");
        if(!iniFile.isFile())
            resetINIFile();
        
        prefProperties = new Properties();
        prefProperties.load(new FileInputStream(iniFile)); 
        formatter = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");
        // Parse preferences properties and load most recent lab 
        parseINI();


        //Set logo icon 
        InputStream inputStream = brokenJavaNaming("labtainer5-sm.png");
        ImageIcon logoImg = new ImageIcon(ImageIO.read(inputStream));

        this.setIconImage(logoImg.getImage());
        logo.setIcon(logoImg);
        // For use in creating new labs
        getBaseImageDockerfiles();   
    }
    private void setMnemonics(){
        FileMenuBar.setMnemonic(java.awt.event.KeyEvent.VK_F);
        OpenLabMenuItem.setMnemonic(java.awt.event.KeyEvent.VK_O);
        NewLabMenuItem.setMnemonic(java.awt.event.KeyEvent.VK_N);
        SaveMenuItem.setMnemonic(java.awt.event.KeyEvent.VK_S);
        SaveAsMenuItem.setMnemonic(java.awt.event.KeyEvent.VK_A);
        PreferencesMenuItem.setMnemonic(java.awt.event.KeyEvent.VK_P);
        ExitMenuItem.setMnemonic(java.awt.event.KeyEvent.VK_X);
        RunMenu.setMnemonic(java.awt.event.KeyEvent.VK_R);
        BuildAndRun.setMnemonic(java.awt.event.KeyEvent.VK_B);
        BuildOnlyMenuItem.setMnemonic(java.awt.event.KeyEvent.VK_Y);
        StopLabMenuItem.setMnemonic(java.awt.event.KeyEvent.VK_T);
        checkWorkMenuItem.setMnemonic(java.awt.event.KeyEvent.VK_C);
        HelpMenu.setMnemonic(java.awt.event.KeyEvent.VK_H);
        ViewMenu.setMnemonic(java.awt.event.KeyEvent.VK_V);
    }
    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        ContainerAddDialog = new javax.swing.JDialog();
        jLabel3 = new javax.swing.JLabel();
        jLabel4 = new javax.swing.JLabel();
        jLabel5 = new javax.swing.JLabel();
        ContainerAddDialogNameTextfield = new javax.swing.JTextField();
        ContainerAddDialogCreateButton = new javax.swing.JButton();
        ContainerAddDialogCancelButton = new javax.swing.JButton();
        ContainerAddDialogBaseImageCombobox = new javax.swing.JComboBox<>();
        NetworkAddDialog = new javax.swing.JDialog();
        jLabel7 = new javax.swing.JLabel();
        jLabel8 = new javax.swing.JLabel();
        jLabel9 = new javax.swing.JLabel();
        jLabel10 = new javax.swing.JLabel();
        jLabel11 = new javax.swing.JLabel();
        jLabel12 = new javax.swing.JLabel();
        jLabel13 = new javax.swing.JLabel();
        NetworkAddDialogNameTextfield = new javax.swing.JTextField();
        NetworkAddDialogMaskTextfield = new javax.swing.JTextField();
        NetworkAddDialogGatewayTextfield = new javax.swing.JTextField();
        NetworkAddDialogIPRangeTextfield = new javax.swing.JTextField();
        NetworkAddDialogCreateButton = new javax.swing.JButton();
        NetworkAddDialogCancelButton = new javax.swing.JButton();
        NetworkAddDialogMacVLanExtSpinner = new javax.swing.JSpinner();
        NetworkAddDialogMacVLanSpinner = new javax.swing.JSpinner();
        NetworkAddDialogTapRadioButton = new javax.swing.JRadioButton();
        labChooser = new javax.swing.JFileChooser();
        NewLabDialog = new javax.swing.JDialog();
        jLabel6 = new javax.swing.JLabel();
        jLabel14 = new javax.swing.JLabel();
        NewLabNameTextfield = new javax.swing.JTextField();
        NewLabBaseImageComboBox = new javax.swing.JComboBox<>();
        NewLabCreateButton = new javax.swing.JButton();
        NewLabCancelButton = new javax.swing.JButton();
        LabExistLabel = new javax.swing.JLabel();
        SaveAsDialog = new javax.swing.JDialog();
        SaveAsLabNameTextField = new javax.swing.JTextField();
        SaveAsErrorLabel = new javax.swing.JLabel();
        SaveAsCancelButton = new javax.swing.JButton();
        SaveAsConfirmButton = new javax.swing.JButton();
        Header = new javax.swing.JPanel();
        LabnameLabel = new javax.swing.JLabel();
        ContainerPanel = new javax.swing.JPanel();
        jLabel1 = new javax.swing.JLabel();
        ContainerScrollPane = new javax.swing.JScrollPane();
        ContainerPanePanel = new javax.swing.JPanel();
        addContainerButton = new javax.swing.JButton();
        NetworkPanel = new javax.swing.JPanel();
        jLabel2 = new javax.swing.JLabel();
        NetworkScrollPane = new javax.swing.JScrollPane();
        NetworkPanePanel = new javax.swing.JPanel();
        addNetworkButton = new javax.swing.JButton();
        logo = new javax.swing.JLabel();
        AssessmentPanel = new javax.swing.JPanel();
        AssessmentButton = new javax.swing.JButton();
        AssessmentButton1 = new javax.swing.JButton();
        IndividualizePanel = new javax.swing.JPanel();
        paramsButton = new javax.swing.JButton();
        jScrollPane1 = new javax.swing.JScrollPane();
        OutputTextArea = new javax.swing.JTextArea();
        MainMenuBar = new javax.swing.JMenuBar();
        FileMenuBar = new javax.swing.JMenu();
        NewLabMenuItem = new javax.swing.JMenuItem();
        jSeparator1 = new javax.swing.JPopupMenu.Separator();
        OpenLabMenuItem = new javax.swing.JMenuItem();
        jSeparator2 = new javax.swing.JPopupMenu.Separator();
        SaveMenuItem = new javax.swing.JMenuItem();
        SaveAsMenuItem = new javax.swing.JMenuItem();
        jSeparator4 = new javax.swing.JPopupMenu.Separator();
        PreferencesMenuItem = new javax.swing.JMenuItem();
        jSeparator5 = new javax.swing.JPopupMenu.Separator();
        ExitMenuItem = new javax.swing.JMenuItem();
        RunMenu = new javax.swing.JMenu();
        BuildAndRun = new javax.swing.JMenuItem();
        BuildOnlyMenuItem = new javax.swing.JMenuItem();
        LocalBuildCheckbox = new javax.swing.JCheckBoxMenuItem();
        StopLabMenuItem = new javax.swing.JMenuItem();
        checkWorkMenuItem = new javax.swing.JMenuItem();
        EditMenu = new javax.swing.JMenu();
        AboutLabMenuItem = new javax.swing.JMenuItem();
        LabDocumentsMenuItem = new javax.swing.JMenuItem();
        readfirstMenu = new javax.swing.JMenuItem();
        SimlabDirectivesMenuItem = new javax.swing.JMenuItem();
        HelpMenu = new javax.swing.JMenu();
        DesignerMenuItem = new javax.swing.JMenuItem();
        StudentMenuItem = new javax.swing.JMenuItem();
        InstructorMenuItem = new javax.swing.JMenuItem();
        ViewMenu = new javax.swing.JMenu();
        labtainerLogMenuItem = new javax.swing.JMenuItem();
        buildMenuItem = new javax.swing.JMenuItem();

        ContainerAddDialog.setTitle("Adding New Container");
        ContainerAddDialog.setMinimumSize(new java.awt.Dimension(433, 220));
        ContainerAddDialog.setResizable(false);

        jLabel3.setFont(new java.awt.Font("Arial", 0, 14)); // NOI18N
        jLabel3.setText("Provide container name and the docker base image used:");

        jLabel4.setFont(new java.awt.Font("Arial", 1, 14)); // NOI18N
        jLabel4.setText("Name: ");

        jLabel5.setFont(new java.awt.Font("Arial", 1, 14)); // NOI18N
        jLabel5.setText("Base Image:");

        ContainerAddDialogNameTextfield.setMinimumSize(new java.awt.Dimension(300, 20));
        ContainerAddDialogNameTextfield.setPreferredSize(new java.awt.Dimension(300, 20));

        ContainerAddDialogCreateButton.setText("Create");
        ContainerAddDialogCreateButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                ContainerAddDialogCreateButtonActionPerformed(evt);
            }
        });

        ContainerAddDialogCancelButton.setText("Cancel");
        ContainerAddDialogCancelButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                ContainerAddDialogCancelButtonActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout ContainerAddDialogLayout = new javax.swing.GroupLayout(ContainerAddDialog.getContentPane());
        ContainerAddDialog.getContentPane().setLayout(ContainerAddDialogLayout);
        ContainerAddDialogLayout.setHorizontalGroup(
            ContainerAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(ContainerAddDialogLayout.createSequentialGroup()
                .addGroup(ContainerAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                    .addGroup(ContainerAddDialogLayout.createSequentialGroup()
                        .addGap(0, 285, Short.MAX_VALUE)
                        .addComponent(ContainerAddDialogCreateButton)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(ContainerAddDialogCancelButton))
                    .addGroup(ContainerAddDialogLayout.createSequentialGroup()
                        .addGroup(ContainerAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addGroup(ContainerAddDialogLayout.createSequentialGroup()
                                .addContainerGap()
                                .addComponent(jLabel3))
                            .addGroup(ContainerAddDialogLayout.createSequentialGroup()
                                .addGap(23, 23, 23)
                                .addGroup(ContainerAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                                    .addGroup(ContainerAddDialogLayout.createSequentialGroup()
                                        .addComponent(jLabel4)
                                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                        .addComponent(ContainerAddDialogNameTextfield, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                                    .addGroup(ContainerAddDialogLayout.createSequentialGroup()
                                        .addComponent(jLabel5)
                                        .addGap(4, 4, 4)
                                        .addComponent(ContainerAddDialogBaseImageCombobox, 0, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)))))
                        .addGap(2, 2, 2)))
                .addContainerGap(24, Short.MAX_VALUE))
        );
        ContainerAddDialogLayout.setVerticalGroup(
            ContainerAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(ContainerAddDialogLayout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jLabel3)
                .addGap(18, 18, 18)
                .addGroup(ContainerAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel4)
                    .addComponent(ContainerAddDialogNameTextfield, javax.swing.GroupLayout.PREFERRED_SIZE, 31, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addGap(10, 10, 10)
                .addGroup(ContainerAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(ContainerAddDialogBaseImageCombobox, javax.swing.GroupLayout.PREFERRED_SIZE, 38, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jLabel5))
                .addGap(18, 18, 18)
                .addGroup(ContainerAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(ContainerAddDialogCreateButton)
                    .addComponent(ContainerAddDialogCancelButton))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        NetworkAddDialog.setTitle("Adding New Network");
        NetworkAddDialog.setMinimumSize(new java.awt.Dimension(400, 380));
        NetworkAddDialog.setResizable(false);

        jLabel7.setFont(new java.awt.Font("Arial", 0, 14)); // NOI18N
        jLabel7.setText("Please fill the sections below to create a new network:");

        jLabel8.setFont(new java.awt.Font("Arial", 1, 14)); // NOI18N
        jLabel8.setText("Gateway:");

        jLabel9.setFont(new java.awt.Font("Arial", 1, 14)); // NOI18N
        jLabel9.setText("Mask:");

        jLabel10.setFont(new java.awt.Font("Arial", 1, 14)); // NOI18N
        jLabel10.setText("IP_Range:");

        jLabel11.setFont(new java.awt.Font("Arial", 1, 14)); // NOI18N
        jLabel11.setText("MACVLAN:");

        jLabel12.setFont(new java.awt.Font("Arial", 1, 14)); // NOI18N
        jLabel12.setText("MACVLAN_EXT:");

        jLabel13.setFont(new java.awt.Font("Arial", 1, 14)); // NOI18N
        jLabel13.setText("Name:");

        NetworkAddDialogNameTextfield.setMinimumSize(new java.awt.Dimension(300, 20));
        NetworkAddDialogNameTextfield.setName(""); // NOI18N
        NetworkAddDialogNameTextfield.setPreferredSize(new java.awt.Dimension(300, 20));

        NetworkAddDialogMaskTextfield.setMinimumSize(new java.awt.Dimension(300, 20));
        NetworkAddDialogMaskTextfield.setName(""); // NOI18N
        NetworkAddDialogMaskTextfield.setPreferredSize(new java.awt.Dimension(300, 20));

        NetworkAddDialogGatewayTextfield.setMinimumSize(new java.awt.Dimension(300, 20));
        NetworkAddDialogGatewayTextfield.setName(""); // NOI18N
        NetworkAddDialogGatewayTextfield.setPreferredSize(new java.awt.Dimension(300, 20));

        NetworkAddDialogIPRangeTextfield.setMinimumSize(new java.awt.Dimension(300, 20));
        NetworkAddDialogIPRangeTextfield.setName(""); // NOI18N
        NetworkAddDialogIPRangeTextfield.setPreferredSize(new java.awt.Dimension(300, 20));

        NetworkAddDialogCreateButton.setText("Create");
        NetworkAddDialogCreateButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                NetworkAddDialogCreateButtonActionPerformed(evt);
            }
        });

        NetworkAddDialogCancelButton.setText("Cancel");
        NetworkAddDialogCancelButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                NetworkAddDialogCancelButtonActionPerformed(evt);
            }
        });

        NetworkAddDialogMacVLanExtSpinner.setFont(new java.awt.Font("Arial", 0, 12)); // NOI18N

        NetworkAddDialogMacVLanSpinner.setFont(new java.awt.Font("Arial", 0, 12)); // NOI18N

        NetworkAddDialogTapRadioButton.setFont(new java.awt.Font("Ubuntu", 1, 18)); // NOI18N
        NetworkAddDialogTapRadioButton.setText("Tap");

        javax.swing.GroupLayout NetworkAddDialogLayout = new javax.swing.GroupLayout(NetworkAddDialog.getContentPane());
        NetworkAddDialog.getContentPane().setLayout(NetworkAddDialogLayout);
        NetworkAddDialogLayout.setHorizontalGroup(
            NetworkAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(NetworkAddDialogLayout.createSequentialGroup()
                .addGroup(NetworkAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(NetworkAddDialogLayout.createSequentialGroup()
                        .addContainerGap()
                        .addComponent(jLabel7))
                    .addGroup(NetworkAddDialogLayout.createSequentialGroup()
                        .addGap(22, 22, 22)
                        .addGroup(NetworkAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addGroup(NetworkAddDialogLayout.createSequentialGroup()
                                .addGroup(NetworkAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                                    .addComponent(jLabel13)
                                    .addComponent(jLabel9))
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                                .addGroup(NetworkAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                    .addComponent(NetworkAddDialogMaskTextfield, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                                    .addComponent(NetworkAddDialogNameTextfield, javax.swing.GroupLayout.PREFERRED_SIZE, 300, javax.swing.GroupLayout.PREFERRED_SIZE)))
                            .addGroup(NetworkAddDialogLayout.createSequentialGroup()
                                .addGap(2, 2, 2)
                                .addGroup(NetworkAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                    .addGroup(NetworkAddDialogLayout.createSequentialGroup()
                                        .addComponent(jLabel8)
                                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                                        .addComponent(NetworkAddDialogGatewayTextfield, javax.swing.GroupLayout.PREFERRED_SIZE, 278, javax.swing.GroupLayout.PREFERRED_SIZE))
                                    .addGroup(NetworkAddDialogLayout.createSequentialGroup()
                                        .addComponent(jLabel12)
                                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                        .addComponent(NetworkAddDialogMacVLanExtSpinner, javax.swing.GroupLayout.PREFERRED_SIZE, 45, javax.swing.GroupLayout.PREFERRED_SIZE))
                                    .addGroup(NetworkAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                                        .addGroup(NetworkAddDialogLayout.createSequentialGroup()
                                            .addComponent(NetworkAddDialogCreateButton)
                                            .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                                            .addComponent(NetworkAddDialogCancelButton))
                                        .addGroup(NetworkAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                            .addComponent(NetworkAddDialogTapRadioButton)
                                            .addGroup(NetworkAddDialogLayout.createSequentialGroup()
                                                .addGroup(NetworkAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                                    .addComponent(jLabel11)
                                                    .addComponent(jLabel10))
                                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                                                .addGroup(NetworkAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                                    .addComponent(NetworkAddDialogIPRangeTextfield, javax.swing.GroupLayout.PREFERRED_SIZE, 269, javax.swing.GroupLayout.PREFERRED_SIZE)
                                                    .addComponent(NetworkAddDialogMacVLanSpinner, javax.swing.GroupLayout.PREFERRED_SIZE, 45, javax.swing.GroupLayout.PREFERRED_SIZE))))))))))
                .addContainerGap(25, Short.MAX_VALUE))
        );
        NetworkAddDialogLayout.setVerticalGroup(
            NetworkAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(NetworkAddDialogLayout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jLabel7)
                .addGap(18, 18, 18)
                .addGroup(NetworkAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel13)
                    .addComponent(NetworkAddDialogNameTextfield, javax.swing.GroupLayout.PREFERRED_SIZE, 30, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(NetworkAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(NetworkAddDialogMaskTextfield, javax.swing.GroupLayout.PREFERRED_SIZE, 30, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jLabel9))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(NetworkAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel8)
                    .addComponent(NetworkAddDialogGatewayTextfield, javax.swing.GroupLayout.PREFERRED_SIZE, 30, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(NetworkAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(NetworkAddDialogMacVLanExtSpinner, javax.swing.GroupLayout.DEFAULT_SIZE, 30, Short.MAX_VALUE)
                    .addComponent(jLabel12))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(NetworkAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel11)
                    .addComponent(NetworkAddDialogMacVLanSpinner, javax.swing.GroupLayout.DEFAULT_SIZE, 30, Short.MAX_VALUE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(NetworkAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(NetworkAddDialogIPRangeTextfield, javax.swing.GroupLayout.PREFERRED_SIZE, 30, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jLabel10))
                .addGap(18, 18, 18)
                .addComponent(NetworkAddDialogTapRadioButton)
                .addGap(2, 2, 2)
                .addGroup(NetworkAddDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(NetworkAddDialogCreateButton)
                    .addComponent(NetworkAddDialogCancelButton))
                .addGap(42, 42, 42))
        );

        labChooser.setCurrentDirectory(null);
        labChooser.setFileSelectionMode(javax.swing.JFileChooser.DIRECTORIES_ONLY);

        NewLabDialog.setTitle("Creating New Lab");
        NewLabDialog.setMinimumSize(new java.awt.Dimension(469, 200));

        jLabel6.setFont(new java.awt.Font("Dialog", 1, 15)); // NOI18N
        jLabel6.setText("Name");

        jLabel14.setFont(new java.awt.Font("Dialog", 1, 15)); // NOI18N
        jLabel14.setText("Base Image");

        NewLabNameTextfield.setFont(new java.awt.Font("Dialog", 0, 15)); // NOI18N

        NewLabCreateButton.setText("Create");
        NewLabCreateButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                NewLabCreateButtonActionPerformed(evt);
            }
        });

        NewLabCancelButton.setText("Cancel");
        NewLabCancelButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                NewLabCancelButtonActionPerformed(evt);
            }
        });

        LabExistLabel.setText("Lab already exists!");

        javax.swing.GroupLayout NewLabDialogLayout = new javax.swing.GroupLayout(NewLabDialog.getContentPane());
        NewLabDialog.getContentPane().setLayout(NewLabDialogLayout);
        NewLabDialogLayout.setHorizontalGroup(
            NewLabDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(NewLabDialogLayout.createSequentialGroup()
                .addGroup(NewLabDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(NewLabDialogLayout.createSequentialGroup()
                        .addGap(20, 20, 20)
                        .addComponent(jLabel6)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(NewLabNameTextfield))
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, NewLabDialogLayout.createSequentialGroup()
                        .addContainerGap()
                        .addGroup(NewLabDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                            .addGroup(NewLabDialogLayout.createSequentialGroup()
                                .addComponent(jLabel14)
                                .addGap(4, 4, 4)
                                .addComponent(NewLabBaseImageComboBox, 0, 344, Short.MAX_VALUE))
                            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, NewLabDialogLayout.createSequentialGroup()
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, 311, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addComponent(NewLabCreateButton)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(NewLabCancelButton)))))
                .addContainerGap())
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, NewLabDialogLayout.createSequentialGroup()
                .addGap(0, 0, Short.MAX_VALUE)
                .addComponent(LabExistLabel)
                .addGap(158, 158, 158))
        );
        NewLabDialogLayout.setVerticalGroup(
            NewLabDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(NewLabDialogLayout.createSequentialGroup()
                .addGap(23, 23, 23)
                .addGroup(NewLabDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel6)
                    .addComponent(NewLabNameTextfield, javax.swing.GroupLayout.PREFERRED_SIZE, 37, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(LabExistLabel)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, 11, Short.MAX_VALUE)
                .addGroup(NewLabDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel14)
                    .addComponent(NewLabBaseImageComboBox, javax.swing.GroupLayout.PREFERRED_SIZE, 40, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(NewLabDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(NewLabCreateButton)
                    .addComponent(NewLabCancelButton))
                .addGap(23, 23, 23))
        );

        SaveAsDialog.setTitle("Save As");
        SaveAsDialog.setMinimumSize(new java.awt.Dimension(400, 140));

        SaveAsLabNameTextField.setFont(new java.awt.Font("Ubuntu", 0, 18)); // NOI18N
        SaveAsLabNameTextField.setHorizontalAlignment(javax.swing.JTextField.CENTER);

        SaveAsErrorLabel.setText("Lab Already Exists!");

        SaveAsCancelButton.setText("Cancel");
        SaveAsCancelButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                SaveAsCancelButtonActionPerformed(evt);
            }
        });

        SaveAsConfirmButton.setText("Confirm");
        SaveAsConfirmButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                SaveAsConfirmButtonActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout SaveAsDialogLayout = new javax.swing.GroupLayout(SaveAsDialog.getContentPane());
        SaveAsDialog.getContentPane().setLayout(SaveAsDialogLayout);
        SaveAsDialogLayout.setHorizontalGroup(
            SaveAsDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(SaveAsDialogLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(SaveAsDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(SaveAsDialogLayout.createSequentialGroup()
                        .addGap(0, 0, Short.MAX_VALUE)
                        .addComponent(SaveAsErrorLabel)
                        .addGap(0, 0, Short.MAX_VALUE))
                    .addComponent(SaveAsLabNameTextField)
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, SaveAsDialogLayout.createSequentialGroup()
                        .addGap(0, 242, Short.MAX_VALUE)
                        .addComponent(SaveAsConfirmButton)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(SaveAsCancelButton)))
                .addContainerGap())
        );
        SaveAsDialogLayout.setVerticalGroup(
            SaveAsDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(SaveAsDialogLayout.createSequentialGroup()
                .addContainerGap()
                .addComponent(SaveAsLabNameTextField, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(SaveAsErrorLabel)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addGroup(SaveAsDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(SaveAsCancelButton)
                    .addComponent(SaveAsConfirmButton))
                .addContainerGap())
        );

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        setTitle("Labtainers");
        setResizable(false);
        addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent evt) {
                formMouseClicked(evt);
            }
        });
        addWindowListener(new java.awt.event.WindowAdapter() {
            public void windowClosing(java.awt.event.WindowEvent evt) {
                MainWindow.this.windowClosing(evt);
            }
        });

        LabnameLabel.setFont(new java.awt.Font("Arial Black", 0, 18)); // NOI18N
        LabnameLabel.setHorizontalAlignment(javax.swing.SwingConstants.LEFT);
        LabnameLabel.setText("Lab:");

        javax.swing.GroupLayout HeaderLayout = new javax.swing.GroupLayout(Header);
        Header.setLayout(HeaderLayout);
        HeaderLayout.setHorizontalGroup(
            HeaderLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, HeaderLayout.createSequentialGroup()
                .addGap(20, 20, 20)
                .addComponent(LabnameLabel, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addGap(831, 831, 831))
        );
        HeaderLayout.setVerticalGroup(
            HeaderLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(HeaderLayout.createSequentialGroup()
                .addContainerGap()
                .addComponent(LabnameLabel)
                .addContainerGap(17, Short.MAX_VALUE))
        );

        ContainerPanel.setBorder(javax.swing.BorderFactory.createEtchedBorder());
        ContainerPanel.setMaximumSize(new java.awt.Dimension(384, 400));
        ContainerPanel.setMinimumSize(new java.awt.Dimension(384, 400));
        ContainerPanel.setPreferredSize(new java.awt.Dimension(384, 400));

        jLabel1.setFont(new java.awt.Font("Arial", 1, 24)); // NOI18N
        jLabel1.setText("Containers");

        ContainerScrollPane.setHorizontalScrollBarPolicy(javax.swing.ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
        ContainerScrollPane.setAutoscrolls(true);

        ContainerPanePanel.setMaximumSize(new java.awt.Dimension(0, 0));
        ContainerPanePanel.setMinimumSize(new java.awt.Dimension(0, 0));
        ContainerPanePanel.setPreferredSize(new java.awt.Dimension(0, 0));
        ContainerPanePanel.setLayout(new java.awt.FlowLayout(java.awt.FlowLayout.CENTER, 5, 0));
        ContainerScrollPane.setViewportView(ContainerPanePanel);

        addContainerButton.setText("Add");
        addContainerButton.setToolTipText("Add a new container.  (Right click containers to change names, delete, etc.)");
        addContainerButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                addContainerButtonActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout ContainerPanelLayout = new javax.swing.GroupLayout(ContainerPanel);
        ContainerPanel.setLayout(ContainerPanelLayout);
        ContainerPanelLayout.setHorizontalGroup(
            ContainerPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(ContainerPanelLayout.createSequentialGroup()
                .addGap(15, 15, 15)
                .addGroup(ContainerPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                    .addComponent(ContainerScrollPane, javax.swing.GroupLayout.DEFAULT_SIZE, 350, Short.MAX_VALUE)
                    .addGroup(ContainerPanelLayout.createSequentialGroup()
                        .addComponent(jLabel1)
                        .addGap(38, 38, 38)
                        .addComponent(addContainerButton, javax.swing.GroupLayout.PREFERRED_SIZE, 82, javax.swing.GroupLayout.PREFERRED_SIZE)))
                .addGap(15, 15, 15))
        );
        ContainerPanelLayout.setVerticalGroup(
            ContainerPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(ContainerPanelLayout.createSequentialGroup()
                .addGap(10, 10, 10)
                .addGroup(ContainerPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jLabel1, javax.swing.GroupLayout.PREFERRED_SIZE, 26, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(addContainerButton))
                .addGap(5, 5, 5)
                .addComponent(ContainerScrollPane)
                .addGap(10, 10, 10))
        );

        NetworkPanel.setBorder(javax.swing.BorderFactory.createEtchedBorder());
        NetworkPanel.setMaximumSize(new java.awt.Dimension(384, 400));
        NetworkPanel.setMinimumSize(new java.awt.Dimension(384, 400));
        NetworkPanel.setPreferredSize(new java.awt.Dimension(384, 400));

        jLabel2.setFont(new java.awt.Font("Arial", 1, 24)); // NOI18N
        jLabel2.setText("Networks");

        NetworkScrollPane.setHorizontalScrollBarPolicy(javax.swing.ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
        NetworkScrollPane.setAutoscrolls(true);

        NetworkPanePanel.setMaximumSize(new java.awt.Dimension(0, 0));
        NetworkPanePanel.setMinimumSize(new java.awt.Dimension(0, 0));
        NetworkPanePanel.setPreferredSize(new java.awt.Dimension(0, 0));
        NetworkPanePanel.setLayout(new java.awt.FlowLayout(java.awt.FlowLayout.CENTER, 5, 0));
        NetworkScrollPane.setViewportView(NetworkPanePanel);

        addNetworkButton.setText("Add");
        addNetworkButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                addNetworkButtonActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout NetworkPanelLayout = new javax.swing.GroupLayout(NetworkPanel);
        NetworkPanel.setLayout(NetworkPanelLayout);
        NetworkPanelLayout.setHorizontalGroup(
            NetworkPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, NetworkPanelLayout.createSequentialGroup()
                .addGap(15, 15, 15)
                .addGroup(NetworkPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                    .addGroup(NetworkPanelLayout.createSequentialGroup()
                        .addComponent(jLabel2)
                        .addGap(41, 41, 41)
                        .addComponent(addNetworkButton, javax.swing.GroupLayout.PREFERRED_SIZE, 82, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addComponent(NetworkScrollPane, javax.swing.GroupLayout.DEFAULT_SIZE, 350, Short.MAX_VALUE))
                .addGap(15, 15, 15))
        );
        NetworkPanelLayout.setVerticalGroup(
            NetworkPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(NetworkPanelLayout.createSequentialGroup()
                .addGap(10, 10, 10)
                .addGroup(NetworkPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jLabel2)
                    .addComponent(addNetworkButton))
                .addGap(5, 5, 5)
                .addComponent(NetworkScrollPane, javax.swing.GroupLayout.DEFAULT_SIZE, 365, Short.MAX_VALUE)
                .addGap(10, 10, 10))
        );

        logo.setText("jLabel17");

        AssessmentPanel.setBorder(javax.swing.BorderFactory.createTitledBorder(null, "Automated Assessment", javax.swing.border.TitledBorder.DEFAULT_JUSTIFICATION, javax.swing.border.TitledBorder.DEFAULT_POSITION, new java.awt.Font("Dialog", 0, 18))); // NOI18N

        AssessmentButton.setText("Results");
        AssessmentButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                ResultsConfigButtonActionPerformed(evt);
            }
        });

        AssessmentButton1.setText("Goals ");
        AssessmentButton1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                GoalsConfigButtonActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout AssessmentPanelLayout = new javax.swing.GroupLayout(AssessmentPanel);
        AssessmentPanel.setLayout(AssessmentPanelLayout);
        AssessmentPanelLayout.setHorizontalGroup(
            AssessmentPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(AssessmentPanelLayout.createSequentialGroup()
                .addGap(25, 25, 25)
                .addGroup(AssessmentPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(AssessmentButton1, javax.swing.GroupLayout.PREFERRED_SIZE, 160, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(AssessmentButton, javax.swing.GroupLayout.PREFERRED_SIZE, 160, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );
        AssessmentPanelLayout.setVerticalGroup(
            AssessmentPanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(AssessmentPanelLayout.createSequentialGroup()
                .addGap(6, 6, 6)
                .addComponent(AssessmentButton)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, 8, Short.MAX_VALUE)
                .addComponent(AssessmentButton1)
                .addContainerGap())
        );

        IndividualizePanel.setBorder(javax.swing.BorderFactory.createTitledBorder(null, "Individualize", javax.swing.border.TitledBorder.CENTER, javax.swing.border.TitledBorder.DEFAULT_POSITION, new java.awt.Font("Dialog", 1, 18))); // NOI18N

        paramsButton.setText("Parameters");
        paramsButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                paramsButtonActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout IndividualizePanelLayout = new javax.swing.GroupLayout(IndividualizePanel);
        IndividualizePanel.setLayout(IndividualizePanelLayout);
        IndividualizePanelLayout.setHorizontalGroup(
            IndividualizePanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 223, Short.MAX_VALUE)
            .addGroup(IndividualizePanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                .addGroup(IndividualizePanelLayout.createSequentialGroup()
                    .addGap(0, 0, Short.MAX_VALUE)
                    .addComponent(paramsButton)
                    .addGap(0, 0, Short.MAX_VALUE)))
        );
        IndividualizePanelLayout.setVerticalGroup(
            IndividualizePanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 52, Short.MAX_VALUE)
            .addGroup(IndividualizePanelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                .addGroup(IndividualizePanelLayout.createSequentialGroup()
                    .addGap(0, 11, Short.MAX_VALUE)
                    .addComponent(paramsButton)
                    .addGap(0, 11, Short.MAX_VALUE)))
        );

        OutputTextArea.setColumns(20);
        OutputTextArea.setRows(5);
        jScrollPane1.setViewportView(OutputTextArea);

        MainMenuBar.setFont(new java.awt.Font("Ubuntu", 0, 48)); // NOI18N

        FileMenuBar.setText("File");
        FileMenuBar.setFont(new java.awt.Font("Ubuntu", 0, 18)); // NOI18N

        NewLabMenuItem.setText("New Lab");
        NewLabMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                NewLabMenuItemActionPerformed(evt);
            }
        });
        FileMenuBar.add(NewLabMenuItem);
        FileMenuBar.add(jSeparator1);

        OpenLabMenuItem.setText("Open Lab");
        OpenLabMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                OpenLabMenuItemActionPerformed(evt);
            }
        });
        FileMenuBar.add(OpenLabMenuItem);
        FileMenuBar.add(jSeparator2);

        SaveMenuItem.setText("Save Lab");
        SaveMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                SaveMenuItemActionPerformed(evt);
            }
        });
        FileMenuBar.add(SaveMenuItem);

        SaveAsMenuItem.setText("Save Lab As");
        SaveAsMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                SaveAsMenuItemActionPerformed(evt);
            }
        });
        FileMenuBar.add(SaveAsMenuItem);
        FileMenuBar.add(jSeparator4);

        PreferencesMenuItem.setText("Preferences");
        PreferencesMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                PreferencesMenuItemActionPerformed(evt);
            }
        });
        FileMenuBar.add(PreferencesMenuItem);
        FileMenuBar.add(jSeparator5);

        ExitMenuItem.setText("Exit");
        ExitMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                ExitMenuItemActionPerformed(evt);
            }
        });
        FileMenuBar.add(ExitMenuItem);

        MainMenuBar.add(FileMenuBar);

        RunMenu.setText("Run");
        RunMenu.setFont(new java.awt.Font("Ubuntu", 0, 18)); // NOI18N

        BuildAndRun.setText("Build and run");
        BuildAndRun.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                BuildAndRunActionPerformed(evt);
            }
        });
        RunMenu.add(BuildAndRun);

        BuildOnlyMenuItem.setText("Build only");
        BuildOnlyMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                BuildOnlyMenuItemActionPerformed(evt);
            }
        });
        RunMenu.add(BuildOnlyMenuItem);

        LocalBuildCheckbox.setText("Local builds");
        LocalBuildCheckbox.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                LocalBuildCheckboxActionPerformed(evt);
            }
        });
        RunMenu.add(LocalBuildCheckbox);

        StopLabMenuItem.setText("Stop lab");
        StopLabMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                StopLabMenuItemActionPerformed(evt);
            }
        });
        RunMenu.add(StopLabMenuItem);

        checkWorkMenuItem.setText("Check work");
        checkWorkMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                checkWorkMenuItemActionPerformed(evt);
            }
        });
        RunMenu.add(checkWorkMenuItem);

        MainMenuBar.add(RunMenu);

        EditMenu.setText("Edit");
        EditMenu.setFont(new java.awt.Font("Ubuntu", 0, 18)); // NOI18N

        AboutLabMenuItem.setText("About this lab");
        AboutLabMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                AboutLabMenuItemActionPerformed(evt);
            }
        });
        EditMenu.add(AboutLabMenuItem);

        LabDocumentsMenuItem.setText("Lab documents");
        LabDocumentsMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                LabDocumentsMenuItemActionPerformed(evt);
            }
        });
        EditMenu.add(LabDocumentsMenuItem);

        readfirstMenu.setText("readfirst.txt");
        readfirstMenu.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                readfirstMenuActionPerformed(evt);
            }
        });
        EditMenu.add(readfirstMenu);

        SimlabDirectivesMenuItem.setText("SimLab directives");
        SimlabDirectivesMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                SimlabDirectivesMenuItemActionPerformed(evt);
            }
        });
        EditMenu.add(SimlabDirectivesMenuItem);

        MainMenuBar.add(EditMenu);

        HelpMenu.setText("Help");
        HelpMenu.setFont(new java.awt.Font("Ubuntu", 0, 18)); // NOI18N

        DesignerMenuItem.setText("Designer Guide");
        DesignerMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                DesignerMenuItemActionPerformed(evt);
            }
        });
        HelpMenu.add(DesignerMenuItem);

        StudentMenuItem.setText("Student Guide");
        StudentMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                StudentMenuItemActionPerformed(evt);
            }
        });
        HelpMenu.add(StudentMenuItem);

        InstructorMenuItem.setText("Instructor Guide");
        InstructorMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                InstructorMenuItemActionPerformed(evt);
            }
        });
        HelpMenu.add(InstructorMenuItem);

        MainMenuBar.add(HelpMenu);

        ViewMenu.setText("View");
        ViewMenu.setFont(new java.awt.Font("Ubuntu", 0, 18)); // NOI18N

        labtainerLogMenuItem.setText("labtainer.log");
        labtainerLogMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                labtainerLogMenuItemActionPerformed(evt);
            }
        });
        ViewMenu.add(labtainerLogMenuItem);

        buildMenuItem.setText("docker_build.log");
        buildMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                buildMenuItemActionPerformed(evt);
            }
        });
        ViewMenu.add(buildMenuItem);

        MainMenuBar.add(ViewMenu);

        setJMenuBar(MainMenuBar);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(Header, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
            .addGroup(layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(ContainerPanel, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(NetworkPanel, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(layout.createSequentialGroup()
                        .addContainerGap()
                        .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 758, javax.swing.GroupLayout.PREFERRED_SIZE)))
                .addGap(14, 14, 14)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(AssessmentPanel, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                        .addGap(0, 0, Short.MAX_VALUE)
                        .addComponent(IndividualizePanel, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(logo, javax.swing.GroupLayout.PREFERRED_SIZE, 201, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(0, 0, Short.MAX_VALUE)))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addComponent(Header, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING, false)
                            .addComponent(NetworkPanel, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.DEFAULT_SIZE, 424, Short.MAX_VALUE)
                            .addComponent(ContainerPanel, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.DEFAULT_SIZE, 424, Short.MAX_VALUE))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(jScrollPane1, javax.swing.GroupLayout.PREFERRED_SIZE, 100, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(AssessmentPanel, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(IndividualizePanel, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                        .addComponent(logo)))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void ResultsConfigButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_ResultsConfigButtonActionPerformed
        resultsConfigButton();
    }//GEN-LAST:event_ResultsConfigButtonActionPerformed

    private void addContainerButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_addContainerButtonActionPerformed
        addContainerButton();
    }//GEN-LAST:event_addContainerButtonActionPerformed
    
    private void addNetworkButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_addNetworkButtonActionPerformed
        addNetworkButton();
    }//GEN-LAST:event_addNetworkButtonActionPerformed

    private void ContainerAddDialogCreateButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_ContainerAddDialogCreateButtonActionPerformed
        addContainerPanel(null);
    }//GEN-LAST:event_ContainerAddDialogCreateButtonActionPerformed
  
    private void NetworkAddDialogCreateButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_NetworkAddDialogCreateButtonActionPerformed
       newNetworkDialogCreateButton();
    }//GEN-LAST:event_NetworkAddDialogCreateButtonActionPerformed
    
    private void OpenLabMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_OpenLabMenuItemActionPerformed
        try {
            openLabButton();
        } catch (IOException ex) {
            Logger.getLogger(MainWindow.class.getName()).log(Level.SEVERE, null, ex);
        }
    }//GEN-LAST:event_OpenLabMenuItemActionPerformed
   
    private void NetworkAddDialogCancelButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_NetworkAddDialogCancelButtonActionPerformed
        NetworkAddDialog.setVisible(false);
    }//GEN-LAST:event_NetworkAddDialogCancelButtonActionPerformed

    private void windowClosing(java.awt.event.WindowEvent evt) {//GEN-FIRST:event_windowClosing
        if(labName != null){
            try{
                saveLab(true);
            } catch (IOException ex) {
                Logger.getLogger(MainWindow.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
        rememberOpenedlab();
    }//GEN-LAST:event_windowClosing
   
    private void NewLabMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_NewLabMenuItemActionPerformed
       newLabButton();
    }//GEN-LAST:event_NewLabMenuItemActionPerformed
   
    private void NewLabCreateButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_NewLabCreateButtonActionPerformed
        createNewLab();
    }//GEN-LAST:event_NewLabCreateButtonActionPerformed

    private void NewLabCancelButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_NewLabCancelButtonActionPerformed
        NewLabDialog.setVisible(false);
    }//GEN-LAST:event_NewLabCancelButtonActionPerformed
    
    private void SaveMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_SaveMenuItemActionPerformed
        if(this.currentLab == null){
            saveAsButton();
        }else{
            try {
                saveLab(false);
            } 
            catch (FileNotFoundException ex) {
                Logger.getLogger(MainWindow.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }//GEN-LAST:event_SaveMenuItemActionPerformed
   
    private void SaveAsMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_SaveAsMenuItemActionPerformed
        saveAsButton();
    }//GEN-LAST:event_SaveAsMenuItemActionPerformed
    
    private void ExitMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_ExitMenuItemActionPerformed
        rememberOpenedlab();
        if(labName != null){
            try{
                saveLab(true);
            } catch (IOException ex) {
                Logger.getLogger(MainWindow.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
        System.exit(0);
    }//GEN-LAST:event_ExitMenuItemActionPerformed

    private void SaveAsCancelButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_SaveAsCancelButtonActionPerformed
        SaveAsDialog.setVisible(false);
    }//GEN-LAST:event_SaveAsCancelButtonActionPerformed

    private void SaveAsConfirmButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_SaveAsConfirmButtonActionPerformed
        saveAsConfirmButton();
    }//GEN-LAST:event_SaveAsConfirmButtonActionPerformed
    
    private void GoalsConfigButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_GoalsConfigButtonActionPerformed
        goalsConfigButton();
    }//GEN-LAST:event_GoalsConfigButtonActionPerformed
    
    private void ContainerAddDialogCancelButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_ContainerAddDialogCancelButtonActionPerformed
        ContainerAddDialog.setVisible(false);
    }//GEN-LAST:event_ContainerAddDialogCancelButtonActionPerformed

    public void doCommand(String cmd){
        ProcessBuilder builder = new ProcessBuilder();
        builder.command("sh", "-c", cmd);
        try{
            Process process = builder.start();
            StreamGobbler streamGobbler = new StreamGobbler(process.getInputStream(), System.out::println);
            Executors.newSingleThreadExecutor().submit(streamGobbler);
            int exitCode = process.waitFor();
            assert exitCode == 0;
        } catch (IOException e){
                System.out.println(e);
        } catch (InterruptedException ie){
                System.out.println(ie);
        }
    }
    public void doLabCommand(String cmd){
        ProcessBuilder builder = new ProcessBuilder();
        builder.command("sh", "-c", cmd);
        File labdir = new File(labsPath+File.separator+this.labName);
        builder.directory(labdir);
        try{
            Process process = builder.start();
            StreamGobbler streamGobbler = new StreamGobbler(process.getInputStream(), System.out::println);
            Executors.newSingleThreadExecutor().submit(streamGobbler);
            int exitCode = process.waitFor();
            assert exitCode == 0;
        } catch (IOException e){
                System.out.println(e);
        } catch (InterruptedException ie){
                System.out.println(ie);
        }
    }
    public String getLastLine(String path) throws IOException{
        String lastLine = "";
        String line;
        BufferedReader br = new BufferedReader(new FileReader(path));
        
        while ((line = br.readLine()) != null) 
        {
            if(line.trim().length() > 0){
                lastLine = line;
            }
        }
        return lastLine;
    }
    public void doStudentCommand(String cmd){
        output(cmd+"\n");
        ProcessBuilder builder = new ProcessBuilder();
        builder.command("sh", "-c", cmd);
        String path = this.labtainerPath+File.separator+"scripts"+File.separator+"labtainer-student";
        builder.directory(new File(path));
        try{
            Process process = builder.start();
            StreamGobbler streamGobbler = new StreamGobbler(process.getInputStream(), System.out::println);
            Executors.newSingleThreadExecutor().submit(streamGobbler);
            int exitCode = process.waitFor();
            System.out.println("exit code is "+exitCode);
            if(exitCode == 0){
                output("Command successful.\n");
            }else{
                output("Command failed, see the labtainer log and/or the docker build log.\n");
                String log_path = this.labtainerPath+File.separator+"logs"+File.separator+"labtainer.log";
                String last = getLastLine(log_path);
                if(last.contains("ERROR")){
                    output(last+"\n");
                }
            }
        } catch (IOException e){
                System.out.println("IOException "+e);
        } catch (InterruptedException ie){
                System.out.println("InterruptedException "+ie);
        }
    }
    private void BuildOnlyMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_BuildOnlyMenuItemActionPerformed
        try {
            saveLab(false);
        } 
        catch (FileNotFoundException ex) {
            Logger.getLogger(MainWindow.class.getName()).log(Level.SEVERE, null, ex);
        }
       
        String cmd = "rebuild -b "+this.labName;
        if(this.LocalBuildCheckbox.isSelected()){
            cmd = "rebuild -b -L "+this.labName;
        }
        //System.out.println("BuildOnly cmd: "+cmd);
        doStudentCommand(cmd);
    }//GEN-LAST:event_BuildOnlyMenuItemActionPerformed

    private void StopLabMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_StopLabMenuItemActionPerformed
        String cmd = "stoplab";
        System.out.println("stoplab");
        doStudentCommand(cmd);
    }//GEN-LAST:event_StopLabMenuItemActionPerformed
    private void openPDF(String fname){
        String cmd = "evince "+fname+" &";
        doCommand(cmd);
    }
    private void DesignerMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_DesignerMenuItemActionPerformed
        String guide = labtainerPath+File.separator+"docs"+File.separator+"labdesigner"+File.separator+"labdesigner.pdf";
        openPDF(guide);
    }//GEN-LAST:event_DesignerMenuItemActionPerformed

    private void StudentMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_StudentMenuItemActionPerformed
        String guide = labtainerPath+File.separator+"docs"+File.separator+"student"+File.separator+"student.pdf";
        openPDF(guide);
    }//GEN-LAST:event_StudentMenuItemActionPerformed

    private void InstructorMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_InstructorMenuItemActionPerformed
        String guide = labtainerPath+File.separator+"docs"+File.separator+"instructor"+File.separator+"instructor.pdf";
        openPDF(guide);
    }//GEN-LAST:event_InstructorMenuItemActionPerformed

    private void labtainerLogMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_labtainerLogMenuItemActionPerformed
        String cmd = "gnome-terminal -t 'labtainer.log' -- tail -f $LABTAINER_DIR/logs/labtainer.log";
        doCommand(cmd);
    }//GEN-LAST:event_labtainerLogMenuItemActionPerformed

    private void buildMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_buildMenuItemActionPerformed
        String cmd = "gnome-terminal -t 'docker_build.log' -- tail -f $LABTAINER_DIR/logs/docker_build.log";
        doCommand(cmd);
    }//GEN-LAST:event_buildMenuItemActionPerformed

    private void checkWorkMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_checkWorkMenuItemActionPerformed
        String path = this.labtainerPath+File.separator+"scripts"+File.separator+"labtainer-student";
        String cmd = "gnome-terminal -t 'checkwork' --working-directory="+path+" -- checkwork -p";
        System.out.println("checkwork cmd "+cmd);
        doCommand(cmd);
    }//GEN-LAST:event_checkWorkMenuItemActionPerformed

    private void paramsButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_paramsButtonActionPerformed
        if(!paramsOpened){
            paramsUI = new ParamsUI(this, false);
            paramsUI.setTitle("Parameters (Individualize) for "+this.labName);
            paramsOpened = true;
        }
    }//GEN-LAST:event_paramsButtonActionPerformed

    private void formMouseClicked(java.awt.event.MouseEvent evt) {//GEN-FIRST:event_formMouseClicked
        //System.out.println("clicked");
        //this.toFront();
    }//GEN-LAST:event_formMouseClicked

    private void BuildAndRunActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_BuildAndRunActionPerformed
        try {
            saveLab(false);
        } 
        catch (FileNotFoundException ex) {
            Logger.getLogger(MainWindow.class.getName()).log(Level.SEVERE, null, ex);
        }
        String cmd = "rebuild "+this.labName;
        if(this.LocalBuildCheckbox.isSelected()){
            cmd = "rebuild -L "+this.labName;
        }
        //System.out.println("BuildAndRun cmd: "+cmd);
        doStudentCommand(cmd);
    }//GEN-LAST:event_BuildAndRunActionPerformed

    private void PreferencesMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_PreferencesMenuItemActionPerformed
        PreferencesPanel panel = new PreferencesPanel();

        panel.setPrefs(this.iniFile, this.prefProperties);
        //panel.setVisible(true);
        JDialog dialog = new JDialog();
        panel.setDialog(dialog);
        //dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
        dialog.setModal(true);
        dialog.add(panel);
        dialog.pack();
        dialog.setLocation(200, 200);
        dialog.setTitle("Labtainers Lab Editor Preferences");
        dialog.setVisible(true);
        dialog.dispose();

    }//GEN-LAST:event_PreferencesMenuItemActionPerformed

    private void AboutLabMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_AboutLabMenuItemActionPerformed
        String aboutPath = this.currentLab.toString()+File.separator+"config"+File.separator+"about.txt";
        String cmd = getTextEditor()+" "+aboutPath+" &";
        doCommand(cmd);
    }//GEN-LAST:event_AboutLabMenuItemActionPerformed

    private void LabDocumentsMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_LabDocumentsMenuItemActionPerformed
        String cmd = "gnome-terminal --working-directory="+currentLab.getPath()+File.separator+"docs";
        System.out.println("cmd: "+cmd);
        doCommand(cmd);
    }//GEN-LAST:event_LabDocumentsMenuItemActionPerformed

    private void SimlabDirectivesMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_SimlabDirectivesMenuItemActionPerformed
        // TODO add your handling code here:
    }//GEN-LAST:event_SimlabDirectivesMenuItemActionPerformed

    private void readfirstMenuActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_readfirstMenuActionPerformed
        String readFirstPath = this.currentLab.toString()+File.separator+"docs"+File.separator+"read_first.txt";
        String cmd = "gnome-terminal -- "+getTextEditor()+readFirstPath+" &";
        doCommand(cmd);
    }//GEN-LAST:event_readfirstMenuActionPerformed

    private void LocalBuildCheckboxActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_LocalBuildCheckboxActionPerformed
        if(this.LocalBuildCheckbox.isSelected()){
            writeValueToINI("localBuild", "true");
        }else{
            writeValueToINI("localBuild", "false");
        }
         
    }//GEN-LAST:event_LocalBuildCheckboxActionPerformed
    
    //BUTTON FUNCTIONS//
    
    // Preps the Container Dialog components and sets the Container Dialog visible
    private void addContainerButton(){
        ContainerAddDialogNameTextfield.setText("");
        ContainerAddDialog.setVisible(true);
    }
    
    // Preps the Network Dialog components and sets the Network Dialog visible
    private void addNetworkButton(){
        NetworkAddDialogGatewayTextfield.setText("");
        NetworkAddDialogIPRangeTextfield.setText("");
        NetworkAddDialogMacVLanExtSpinner.setValue(0);
        NetworkAddDialogMacVLanSpinner.setValue(0);
        NetworkAddDialogMaskTextfield.setText("");
        NetworkAddDialogNameTextfield.setText("");
        NetworkAddDialogTapRadioButton.setSelected(false);
        NetworkAddDialog.setVisible(true);
    }
    
    // Adds new Network to the data state and the UI
    private void newNetworkDialogCreateButton(){
        //Create new networkData object here based on the field info
        LabData.NetworkData newNetworkData = new LabData.NetworkData(
            NetworkAddDialogNameTextfield.getText().toUpperCase(),
            NetworkAddDialogMaskTextfield.getText(),
            NetworkAddDialogGatewayTextfield.getText(),
            (int)NetworkAddDialogMacVLanExtSpinner.getValue(),
            (int)NetworkAddDialogMacVLanSpinner.getValue(),
            NetworkAddDialogTapRadioButton.isSelected()
        );
        
        // Update the list of labs in the current UI data object
        labDataCurrent.getNetworks().add(newNetworkData);
        
        // Add the network into the UI 
        addNetworkPanel(newNetworkData);
        
        // Update the Container Config dialogs to include the new network
        updateNetworkReferenceInContainerConfigDialogs("Add", NetworkAddDialogNameTextfield.getText().toUpperCase(), null);
    }
 
    // Opens up file chooser window that defaults to the labs directory relative to the set labtainerPath
    // and opens the lab based on the lab directory chosen
    private void openLabButton() throws IOException{
        if(labName != null){
            try{
                saveLab(true);
            } catch (IOException ex) {
                Logger.getLogger(MainWindow.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
        labChooser.setCurrentDirectory(labsPath);   
        int returnVal = labChooser.showOpenDialog(this);
        if (returnVal == JFileChooser.APPROVE_OPTION) {
            File lab = labChooser.getSelectedFile();
            while(!lab.getParent().endsWith(File.separator+"labs")){
                lab = new File(lab.getParent());
            }
            openLab(lab);
        } 
    }
    
    // Preps the NewLab Dialog and makes it visible
    private void newLabButton(){
        if(labName != null){
            try{
                saveLab(true);
            } catch (IOException ex) {
                Logger.getLogger(MainWindow.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
        NewLabNameTextfield.setText("");
        NewLabDialog.setVisible(true);
        NewLabNameTextfield.requestFocusInWindow();
    }
    
    
    // Preps Save As Dialog and makes it visible
    private void saveAsButton(){
        SaveAsLabNameTextField.setText("");
        SaveAsErrorLabel.setVisible(false);
        SaveAsDialog.setVisible(true);
    } 
    
    // Checks if save lab as input is valid: makes a saveas() call if valid, and displays error message if otherwise
    private void saveAsConfirmButton(){
       //Check if the input is valid (lcase and no spaces)
        String input = SaveAsLabNameTextField.getText();
        
        if(input.contains(" ") || !input.equals(input.toLowerCase())){            
            SaveAsErrorLabel.setText("Lab name must be lowercase and contain no spaces!");
            SaveAsErrorLabel.setVisible(true);
        }
        //Check if lab already exists
        else if(Arrays.asList(labsPath.list()).contains(input)){ 
            SaveAsErrorLabel.setText("Lab already exists!");
            SaveAsErrorLabel.setVisible(true);
        }
        else{
            SaveAsErrorLabel.setVisible(false);
            saveAs(input);
            SaveAsDialog.setVisible(false);
        } 
    }
    
    // Creates, Loads, and Opens Results Configuration UI
    private void resultsConfigButton(){
       if(!resultsOpened){
            resultsUI = new ResultsUI(this, false);
            resultsUI.setTitle("Results for "+this.labName);
            resultsOpened = true;
        } 
    }
    
    // Creates, Loads, and Opens the Goals Configuration UI
    private void goalsConfigButton(){
        if(!goalsOpened){
            goalsUI = new GoalsUI(this, false);
            goalsUI.setTitle("Goals for "+this.labName);
            goalsOpened = true;
        }
    }
    
    // CORE FUNCTIONS //
    
    public int containerPanePanelLength = 0;
    private final JScrollBar containerScrollPaneBar;
    private void addContainerPanel(ContainerData data){
        // Create the Container Obj Panel and add it
        ContainerObjPanel newContainer;
        // If null then this is a new container being added
        if(data == null){
            String containerName = ContainerAddDialogNameTextfield.getText(); 
            if(containerName == null || containerName.trim().length() == 0){
                System.out.println("No container name provided.");
                return;
            }
            String baseImage = (String)ContainerAddDialogBaseImageCombobox.getSelectedItem();
            ContainerData freshContainerData = new ContainerData(containerName);
            newContainer = new ContainerObjPanel(this, freshContainerData);
            
            // Update the data object to include the new container
            labDataCurrent.getContainers().add(freshContainerData);
            ResultsData.containerList.add(containerName);
            
            // Update the Results UI to include the new container
            if(resultsUI!= null)
                resultsUI.refresh();
            
            // Add the container into the user's file system
            addContainer(containerName, baseImage);
            newContainer.setNameLabel();
        }
        else {
            newContainer = new ContainerObjPanel(this, data);
        }

        // Resize the JPanel holding all the ContainerObjPanels to fit another ContainerObjPanel 
        containerPanePanelLength+=50;
        ContainerPanePanel.setPreferredSize(new Dimension(0,containerPanePanelLength));
        ContainerPanePanel.add(newContainer);
        
        // Redraw GUI with the new Panel
        ContainerPanePanel.revalidate();
        ContainerPanePanel.repaint(); 
        
        // Lower the Scroll Bar to show the newly added container. BUG[6/25/20]: still always off by a single panel
        containerScrollPaneBar.setValue(50+containerScrollPaneBar.getMaximum());
        
        // Make the Container Add Dialog Invisible
        ContainerAddDialog.setVisible(false);
    }

    // Adds the container in the lab directory structure by calling 'new_lab_setup.py -a containername -b baseImage'
    private void addContainer(String containerName, String baseImage){
                // Call python new_lab_script: new_lab_setup.py -b basename
                //String cmd = "./addContainer.sh "+labsPath+" "+labName+" "+containerName+" "+baseImage;
                String cmd = "new_lab_setup.py -a "+containerName+" -b "+baseImage;
                doLabCommand(cmd);
    }
    
    public int networkPanePanelLength = 0;
    private JScrollBar networkScrollPaneBar;
    private void addNetworkPanel(NetworkData data){
        //Resize the JPanel Holding all the NetworkObjPanels to fit another NetworkObjPanel
        //[BUG: 6/25/2020] Not sure Why but the network obj panel needs to be 1 px taller than the container panel to be the same size
        networkPanePanelLength+=51;
        NetworkPanePanel.setPreferredSize(new Dimension(0,networkPanePanelLength));
        
        // Create the Network Obj Panel and add it
        NetworkPanePanel.add(new NetworkObjPanel(this, data));        
        
        // Redraw GUI with the new Panel
        NetworkPanePanel.revalidate();
        NetworkPanePanel.repaint(); 
        
        //Lower the Scroll Bar to show the newly added container (BUG[6/25/20]: still always off by a single panel)
        networkScrollPaneBar.setValue(networkScrollPaneBar.getMaximum());
        
        // Make the Network Add Dialog Disappear
        NetworkAddDialog.setVisible(false);
    }    
    private void checkManual() throws IOException{
        String readFirstPath = this.currentLab.toString()+File.separator+"docs"+File.separator+"read_first.txt";
        BufferedReader br = null;
        try{
            br = new BufferedReader(new FileReader(readFirstPath));
        }catch(FileNotFoundException ex){
            output("Missing file at "+readFirstPath);
            return;
        }
        String docname = null; 
        String line;
        while ((line = br.readLine()) != null) 
        {
           if(line.trim().startsWith("file://LAB_DOCS")){ 
               docname = line.substring(line.lastIndexOf(File.separator)+1);
               break;
           }else if(line.contains("LAB_MANUAL")){
               docname = this.labName+".pdf";
               break;
           }
        }
        if(docname != null){ 
            String manualPath = currentLab.toString()+File.separator+"docs"+File.separator+docname;
            File manual = new File(manualPath);
            if(! manual.exists()){
                output("No lab manual found at docs/"+docname+" Use 'Edit=>Lab documents' and create a lab manual there, or\n");
                output("change the name in read_first.txt to match your lab manual.\n");
            }
        }else{
            output("No link to a lab manual found in "+readFirstPath+"\n");
            output("path should include: file://LAB_DOCS/<your manaul");
        }
        String aboutPath = this.currentLab.toString()+File.separator+"config"+File.separator+"about.txt";
        File aboutFile = new File(aboutPath);
        if(!aboutFile.exists()){
            output("No about.txt found for this lab.\n");
        }
    }
    // Loads data and UI for the selected lab
    private void openLab(File lab) throws IOException{        
        // Load data
        this.currentLab = lab;
        this.labName = lab.toString().substring(lab.toString().lastIndexOf(File.separator)+1);
        this.labDataCurrent = new LabData(this, lab, labName); 
        outputClear();
        // Load UI
        closeAllDialogs(); 
        resetWindow();
        loadLab();
        checkManual();
        
    }    
    
    // Creates new lab and opens it
    private void createNewLab(){
        String newLabName = NewLabNameTextfield.getText();
        // If lab doesn't exist make the new lab
        outputClear();
        if(!Arrays.asList(labsPath.list()).contains(newLabName)){ 
            try{
                LabExistLabel.setVisible(false);
                NewLabDialog.revalidate();
                //call python new_lab_script: new_lab_setup.py -b basename              
                File labdir = new File(labsPath+File.separator+newLabName);
                labdir.mkdir();
                this.labName = newLabName;
                String cmd = "new_lab_setup.py -b "+NewLabBaseImageComboBox.getSelectedItem();
                doLabCommand(cmd);
                
                // Close the new lab dialog and open the new lab
                NewLabDialog.setVisible(false);
                openLab(new File(labsPath+File.separator+newLabName));
            } 
            catch (IOException e){
                System.out.println(e);
            }
        }
        else{
            LabExistLabel.setVisible(true);
            NewLabDialog.revalidate();
            System.out.println("Lab already exists. Make the lab with a different name other than:");
            printExistingLabs();
        }
    }
    private String getStartConfigPath(){
        String retval = currentLab.getPath()+File.separator+"config"+File.separator+"start.config";
        return retval;
    }
    boolean deleteDirectory(File directoryToBeDeleted) {
        File[] allContents = directoryToBeDeleted.listFiles();
        if (allContents != null) {
            for (File file : allContents) {
                deleteDirectory(file);
            }
        }
        return directoryToBeDeleted.delete();
    }
    private void rmTmp(String f1, String f2){
        if(f1 != null && f2 != null){
            String parts[] = f1.split(File.separator);
            String next = parts[2];
            String tdir = File.separator+"tmp"+File.separator+next;
            File tdirFile = new File(tdir);
            deleteDirectory(tdirFile);
            parts = f2.split(File.separator);
            next = parts[2];
            tdir = File.separator+"tmp"+File.separator+next;
            tdirFile = new File(tdir);
            deleteDirectory(tdirFile);
        }
    }
         
    // Writes current state of the UI the file system
    private boolean saveLab(boolean usetmp) throws FileNotFoundException{
        // If usetmp, save to temporary diretory and compare to current.  If they differ,
        // prompts the user to save or discard changes.
        // Return false if user cancels (does not want to exit).
        boolean retval = true;
        // Cycle through network objects and save UI to database (not files yet)
        Component[] networks = NetworkPanePanel.getComponents();
        for(Component network : networks){
            NetworkObjPanel panel = (NetworkObjPanel)network;
            if(panel.configShowing()){
                System.out.println("network visible"); 
                panel.networkConfigUpdateButton();
            }
        }
        
        // Cycle through container objects and save UI
        Component[] containers = ContainerPanePanel.getComponents();
        for(Component container : containers){
            ContainerObjPanel panel = (ContainerObjPanel)container;
            if(panel.configShowing()){
                System.out.println("container visible"); 
                panel.updateData();
            }
        }
        
        if(usetmp){ 
            String f1 = null;
            String f2 = null;
            boolean something_changed = true;
            LabData labDataOrig = null;
            try{
                labDataOrig = new LabData(this, this.currentLab, labName); 
                f1 = labDataCurrent.writeStartConfig(usetmp);
                f2 = labDataOrig.writeStartConfig(usetmp);
                something_changed = ! CompareTextFiles.compare(f1, f2);
                rmTmp(f1, f2);
                
            }catch(IOException ex){
                System.out.println("Error comparing start files "+f1+" and "+f2+" "+ex);
            }
            if(!something_changed){
                f1 = labDataCurrent.getResultsData().writeResultsConfig(usetmp);
                f2 = labDataOrig.getResultsData().writeResultsConfig(usetmp);
                try{
                    something_changed = ! CompareTextFiles.compare(f1, f2);
                }catch(IOException ex){
                    System.out.println("Error comparing results config files "+f1+" and "+f2);
                }
                rmTmp(f1, f2);
            }
            if(!something_changed){
                f1 = labDataCurrent.getGoalsData().writeGoalsConfig(usetmp);
                f2 = labDataOrig.getGoalsData().writeGoalsConfig(usetmp);
                try{
                    something_changed = ! CompareTextFiles.compare(f1, f2);
                }catch(IOException ex){
                    System.out.println("Error comparing goals config files "+f1+" and "+f2);
                }
                rmTmp(f1, f2);
            }
            if(!something_changed){
                f1 = labDataCurrent.getParamsData().writeParamsConfig(usetmp);
                f2 = labDataOrig.getParamsData().writeParamsConfig(usetmp);
                try{
                    something_changed = ! CompareTextFiles.compare(f1, f2);
                }catch(IOException ex){
                    System.out.println("Error comparing parameter config files "+f1+" and "+f2);
                }
                rmTmp(f1, f2);
            }
             
            if(something_changed){
                //int confirm = JOptionPane.showConfirmDialog(null, "Changes made to lab config files have not been saved. Save them?\n",
                //                                        "Save changes?",  JOptionPane.YES_NO_CANCEL_OPTION);
                int confirm = JOptionPane.showConfirmDialog(null, "Changes made to lab config files have not been saved. Save them?\n",
                                                        "Save changes?",  JOptionPane.YES_NO_OPTION);
                if (confirm == JOptionPane.YES_OPTION){
                    System.out.println("Saved changes");
                    saveLab(false);
                //}else if(confirm == JOptionPane.CANCEL_OPTION){
                //    retval = false;
                }
            }
        }else{
            labDataCurrent.writeStartConfig(usetmp);
            labDataCurrent.getResultsData().writeResultsConfig(usetmp);
            labDataCurrent.getGoalsData().writeGoalsConfig(usetmp);
            labDataCurrent.getParamsData().writeParamsConfig(usetmp);
        }
        //System.out.println("Lab Saved (or not)");
        return retval;
    }
    
    // Clones the current lab into a new lab
    private void saveAs(String newLabName) {
        // Call Clone Script, feeding in the new lab name
            // Call python new_lab_script: new_lab_setup.py -c newLabName
            String cmd = "new_lab_setup.py -c "+newLabName;
            doLabCommand(cmd); 
            // Rename to current lab and set the path to the new lab
            this.labName = newLabName;
            LabnameLabel.setText("Lab: "+this.labName);
            this.currentLab = new File(labsPath+File.separator+this.labName);
            this.labDataCurrent.setName(this.labName);
            this.labDataCurrent.setPath(this.currentLab);

            // Write the current state to the new lab's start.config
            try {
                saveLab(false);
            } 
            catch (FileNotFoundException ex) {
                Logger.getLogger(MainWindow.class.getName()).log(Level.SEVERE, null, ex);
            }
            
            // Make the Save As Dialo disappear
            SaveAsDialog.setVisible(false);
    }
    
    
    
    // Update all references to the labtainerPath to the current labtainerPath
    public void updateLabtainersPath(){
        labsPath = new File(labtainerPath + File.separator + "labs");
    }
    
    // Parses the main.ini file to set the labtainers path and checks if we load a previous lab
    private void parseINI() throws IOException{
        // If the labtainersPath not set in the main.ini file, set it to the System environmenta variable LABTAINER_DIR 
        labtainerPath = prefProperties.getProperty("labtainerPath");
        if(labtainerPath == null || labtainerPath.isEmpty()){
            System.out.println("No labtainer path set yet");
            labtainerPath = System.getenv("LABTAINER_DIR");
            FileOutputStream out = new FileOutputStream(iniFile);
            writeValueToINI("labtainerPath", System.getenv("LABTAINER_DIR"));
        }
        else{
            labtainerPath.trim();
        }

        // If textEditorPref is empty, set it to 'vi' and write to the main.ini file
        textEditorPref = prefProperties.getProperty("textEditor");
        if(textEditorPref == null || textEditorPref.isEmpty() || textEditorPref.equals("vi")){
            textEditorPref = "gnome-terminal -- vi";
            writeValueToINI("textEditor", textEditorPref);
        }
        else{
            textEditorPref.trim();
        }

        updateLabtainersPath();

        // If a lab has been loaded before then load that lab
        String iniPrevLab = prefProperties.getProperty("prevLab");
        if(iniPrevLab != null && !iniPrevLab.isEmpty()){
            File prevLab = new File(iniPrevLab);
            if(prevLab.isDirectory())
                openLab(prevLab);
        }else{
            File defaultLab = new File(labsPath+File.separator+"telnetlab");
            openLab(defaultLab);
        }
        String localBuild = prefProperties.getProperty("localBuild");
        if(localBuild == null){
            writeValueToINI("localBuild", "false");
        }else if(localBuild == "true"){
            this.LocalBuildCheckbox.setSelected(true);
        }else{
            this.LocalBuildCheckbox.setSelected(true);
        }
        
    }
    private InputStream brokenJavaNaming(String resource){
        ClassLoader classloader = Thread.currentThread().getContextClassLoader();
        InputStream inputStream = classloader.getResourceAsStream(resource);
        if(inputStream == null){
            inputStream = classloader.getResourceAsStream("MainUI/src/main/resources/"+resource);
            if(inputStream == null){
                System.out.println("Could not find resource "+resource);
            }
        }
        return inputStream;
    } 
    // Get list of base images for making new lab and set ui elements that uses them as input
    private void getBaseImageDockerfiles(){
        ArrayList<String> baseList = new ArrayList<String>();
        InputStream inputStream = brokenJavaNaming("base.list");
        if(inputStream == null){
            System.out.println("No base.list file found.");
        }else{
            InputStreamReader streamReader = new InputStreamReader(inputStream, StandardCharsets.UTF_8);
            BufferedReader reader = new BufferedReader(streamReader);
            try{
                for (String line; (line = reader.readLine()) != null;) {
                    baseList.add(line);
                } 
            }catch(IOException ex){
                System.out.println(ex);
            }
        }

        // Get list of valid base dockerfiles
        File dockerfileBasesPath = new File(labtainerPath + File.separator +"scripts"+ File.separator+"designer"+File.separator+"base_dockerfiles");
        File[] baseFiles = dockerfileBasesPath.listFiles(new FilenameFilter(){
            public boolean accept(File dockerfileBasesPath, String filename)
                {return filename.startsWith("Dockerfile.labtainer."); }
        } );
        
        for(int i = 0;i<baseFiles.length;i++){
            String base = baseFiles[i].getName().split("Dockerfile.labtainer.")[1];
            if(!baseList.contains(base)){
                baseList.add(base);
            }
        }
        Collections.sort(baseList); 
        //Set the base image combobox options for making new labs and adding containers
        for(String baseImage : baseList){
            NewLabBaseImageComboBox.addItem(baseImage);
            ContainerAddDialogBaseImageCombobox.addItem(baseImage);
        }
    }

    // Save the current lab reference into the main.ini
    private void rememberOpenedlab(){
        try {
            if(currentLab != null){
                writeValueToINI("prevLab", currentLab.getPath());
            }
            else{
                writeValueToINI("prevLab", "");
            }
            
        }
        catch (NullPointerException ex) {
            System.out.println(ex);
        }
    }
   
    // Sets the main.ini file to the backup
    // Code taken from Beginners Book: https://beginnersbook.com/2014/05/how-to-copy-a-file-to-another-file-in-java/
    private void resetINIFile(){
	FileOutputStream outstream = null;
        System.out.println("do reset");
        InputStream instream = brokenJavaNaming("UI.ini");
        if (instream == null){
            System.out.println("instream null looking for UI.ini");
            System.exit(1);
        }
 
    	try{
    	    File outfile = iniFile;
 
    	    outstream = new FileOutputStream(outfile);
 
    	    byte[] buffer = new byte[1024];
 
    	    int length;
    	    /*copying the contents from input stream to
    	     * output stream using read and write methods
    	     */
    	    while ((length = instream.read(buffer)) > 0){
    	    	outstream.write(buffer, 0, length);
    	    }

    	    //Closing the input/output file streams
    	    instream.close();
    	    outstream.close();
    	    
            System.out.println("File copied successfully!!");
 
    	}catch(IOException ioe){
    		ioe.printStackTrace();
    	 }
    }
     
    // Writes a value to a key in the main.ini file 
    private void writeValueToINI(String key, String value){
        try{
            // update the labtainerPath property
            //prefProperties.load(new FileInputStream(iniFile)); 
            prefProperties.put(key, value);

            // write update to the ini File
            date = new Date();
            FileOutputStream out = new FileOutputStream(this.iniFile);
            prefProperties.store(out, "Updated: "+ formatter.format(date));
            out.close();
    	}catch(IOException ioe){
    		output("Error writing to INI file "+ioe+"\n");
    	}
    }
    
    // Clears the panels of Containers and Networks
    private void resetWindow(){
        // Clear Container Panel
        Component[] componentList = ContainerPanePanel.getComponents();
        for(Component c: componentList)
            ContainerPanePanel.remove(c);
        
        containerPanePanelLength=0;
        ContainerPanePanel.setPreferredSize(new Dimension(0,containerPanePanelLength));
        
        // Clear Network Panel
        componentList = NetworkPanePanel.getComponents();
        for(Component c: componentList)
            NetworkPanePanel.remove(c);
        
        networkPanePanelLength=0;
        NetworkPanePanel.setPreferredSize(new Dimension(0,networkPanePanelLength));
        
        this.revalidate();
        this.repaint();
    }
    
    // Load the data into the UI
    private void loadLab(){
        LabnameLabel.setText("Lab: "+labDataCurrent.getName());
        
        // Load the networks 
        for(int i = 0;i<labDataCurrent.getNetworks().size();i++){
            addNetworkPanel(labDataCurrent.getNetworks().get(i));
        }
        
        //Load the containers 
        for(int i = 0;i<labDataCurrent.getContainers().size();i++){
            addContainerPanel(labDataCurrent.getContainers().get(i));
        }
    }  
    
    //Closes/disposes all windows for the current lab
    //Limitations: Doesn't close the terminal window used to edit a dockerfile for a container
    private void closeAllDialogs(){
        if(resultsUI != null){
            resultsUI.dispose();
            setResultsClosed();
        }
        if(goalsUI != null){
            goalsUI.dispose();
            setGoalsClosed();
        }
        if(paramsUI != null){
            paramsUI.dispose();
            setParamsClosed();
        }
        
        for(Component container : ContainerPanePanel.getComponents()){
            ((ContainerObjPanel)container).getContainerConfigDialog().dispose();
        }
        
        for(Component network : NetworkPanePanel.getComponents()){
            ((NetworkObjPanel)network).getNetworkConfigDialog().dispose();
        }
    }
    
    
    //PUBLIC FUNCTIONS (getters,setters, etc)
    
    public LabData getCurrentData(){
        return labDataCurrent;
    }
    
    public File getCurrentLab(){
        return currentLab;
    }
    
    public ResultsUI getResultsUI(){
        return resultsUI;
    }
    
    public File getLabsPath(){
        return labsPath;
    }
    
    public String getLabName(){
        return labName;
    }
          
    public void setResultsClosed(){
        resultsOpened = false;
    }
    
    public void setGoalsClosed(){
        goalsOpened = false;
    }
    public void setParamsClosed(){
        paramsOpened = false;
    }

    public void updateParameters(){
        if(goalsOpened){
            goalsUI.updateParameters();
        }
    }
    
    public void printExistingLabs(){
        int labCount = 1;
        for(String lab : labsPath.list()){
            System.out.print(lab + ", ");
            if(labCount % 5 == 0){
                System.out.println();
            }
            labCount++;
        }
    }
    
    // Updates the combobox items in the Container Config Windows during a network renaming
    public void updateNetworkReferenceInContainerConfigDialogs(String type, String network, String network2){
        for(Component container : ContainerPanePanel.getComponents()){
            ((ContainerObjPanel)container).updateNetworkComboBoxes(type, network, network2);
        }
    }
    public void outputClear(){
        OutputTextArea.setText("");
    } 
    public void output(String line){
        OutputTextArea.append(line);
        OutputTextArea.requestFocus();
    }
    public String getTextEditor(){
        return prefProperties.getProperty("textEditor")+" ";
    }
    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(MainWindow.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(MainWindow.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(MainWindow.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(MainWindow.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                try {
                    new MainWindow().setVisible(true);
                } catch (IOException ex) {
                    System.out.println(ex);
                }
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JMenuItem AboutLabMenuItem;
    private javax.swing.JButton AssessmentButton;
    private javax.swing.JButton AssessmentButton1;
    private javax.swing.JPanel AssessmentPanel;
    private javax.swing.JMenuItem BuildAndRun;
    private javax.swing.JMenuItem BuildOnlyMenuItem;
    private javax.swing.JDialog ContainerAddDialog;
    private javax.swing.JComboBox<String> ContainerAddDialogBaseImageCombobox;
    private javax.swing.JButton ContainerAddDialogCancelButton;
    private javax.swing.JButton ContainerAddDialogCreateButton;
    private javax.swing.JTextField ContainerAddDialogNameTextfield;
    private javax.swing.JPanel ContainerPanePanel;
    private javax.swing.JPanel ContainerPanel;
    private javax.swing.JScrollPane ContainerScrollPane;
    private javax.swing.JMenuItem DesignerMenuItem;
    private javax.swing.JMenu EditMenu;
    private javax.swing.JMenuItem ExitMenuItem;
    private javax.swing.JMenu FileMenuBar;
    private javax.swing.JPanel Header;
    private javax.swing.JMenu HelpMenu;
    private javax.swing.JPanel IndividualizePanel;
    private javax.swing.JMenuItem InstructorMenuItem;
    private javax.swing.JMenuItem LabDocumentsMenuItem;
    private javax.swing.JLabel LabExistLabel;
    private javax.swing.JLabel LabnameLabel;
    private javax.swing.JCheckBoxMenuItem LocalBuildCheckbox;
    private javax.swing.JMenuBar MainMenuBar;
    private javax.swing.JDialog NetworkAddDialog;
    private javax.swing.JButton NetworkAddDialogCancelButton;
    private javax.swing.JButton NetworkAddDialogCreateButton;
    private javax.swing.JTextField NetworkAddDialogGatewayTextfield;
    private javax.swing.JTextField NetworkAddDialogIPRangeTextfield;
    private javax.swing.JSpinner NetworkAddDialogMacVLanExtSpinner;
    private javax.swing.JSpinner NetworkAddDialogMacVLanSpinner;
    private javax.swing.JTextField NetworkAddDialogMaskTextfield;
    private javax.swing.JTextField NetworkAddDialogNameTextfield;
    private javax.swing.JRadioButton NetworkAddDialogTapRadioButton;
    private javax.swing.JPanel NetworkPanePanel;
    private javax.swing.JPanel NetworkPanel;
    private javax.swing.JScrollPane NetworkScrollPane;
    private javax.swing.JComboBox<String> NewLabBaseImageComboBox;
    private javax.swing.JButton NewLabCancelButton;
    private javax.swing.JButton NewLabCreateButton;
    private javax.swing.JDialog NewLabDialog;
    private javax.swing.JMenuItem NewLabMenuItem;
    private javax.swing.JTextField NewLabNameTextfield;
    private javax.swing.JMenuItem OpenLabMenuItem;
    private javax.swing.JTextArea OutputTextArea;
    private javax.swing.JMenuItem PreferencesMenuItem;
    private javax.swing.JMenu RunMenu;
    private javax.swing.JButton SaveAsCancelButton;
    private javax.swing.JButton SaveAsConfirmButton;
    private javax.swing.JDialog SaveAsDialog;
    private javax.swing.JLabel SaveAsErrorLabel;
    private javax.swing.JTextField SaveAsLabNameTextField;
    private javax.swing.JMenuItem SaveAsMenuItem;
    private javax.swing.JMenuItem SaveMenuItem;
    private javax.swing.JMenuItem SimlabDirectivesMenuItem;
    private javax.swing.JMenuItem StopLabMenuItem;
    private javax.swing.JMenuItem StudentMenuItem;
    private javax.swing.JMenu ViewMenu;
    private javax.swing.JButton addContainerButton;
    private javax.swing.JButton addNetworkButton;
    private javax.swing.JMenuItem buildMenuItem;
    private javax.swing.JMenuItem checkWorkMenuItem;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel10;
    private javax.swing.JLabel jLabel11;
    private javax.swing.JLabel jLabel12;
    private javax.swing.JLabel jLabel13;
    private javax.swing.JLabel jLabel14;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JLabel jLabel3;
    private javax.swing.JLabel jLabel4;
    private javax.swing.JLabel jLabel5;
    private javax.swing.JLabel jLabel6;
    private javax.swing.JLabel jLabel7;
    private javax.swing.JLabel jLabel8;
    private javax.swing.JLabel jLabel9;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JPopupMenu.Separator jSeparator1;
    private javax.swing.JPopupMenu.Separator jSeparator2;
    private javax.swing.JPopupMenu.Separator jSeparator4;
    private javax.swing.JPopupMenu.Separator jSeparator5;
    private javax.swing.JFileChooser labChooser;
    private javax.swing.JMenuItem labtainerLogMenuItem;
    private javax.swing.JLabel logo;
    private javax.swing.JButton paramsButton;
    private javax.swing.JMenuItem readfirstMenu;
    // End of variables declaration//GEN-END:variables

    private static class StreamGobbler implements Runnable {
        private InputStream inputStream;
        private Consumer<String> consumer;
 
        public StreamGobbler(InputStream inputStream, Consumer<String> consumer) {
            this.inputStream = inputStream;
            this.consumer = consumer;
        }
 
        @Override
        public void run() {
            new BufferedReader(new InputStreamReader(inputStream)).lines()
              .forEach(consumer);
        }
    }
}
