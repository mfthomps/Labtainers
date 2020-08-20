/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package labtainers.mainui;

import java.awt.Component;
import java.awt.Dimension;
import java.awt.List;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.FilenameFilter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Properties;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JFileChooser;
import javax.swing.JPanel;
import javax.swing.JScrollBar;
import labtainers.mainui.LabData.ContainerData;
import labtainers.mainui.LabData.NetworkData;
import java.util.ArrayList;
import java.util.Arrays;
import javax.swing.ImageIcon;


/**
 *
 * @author Daniel Liao
 */
public class MainWindow extends javax.swing.JFrame {

    /**
     * Creates new form MainWindow
     */
    LabData labDataSaved;
    LabData labDataCurrent;
    String labtainerPath;
    File labsPath;
    String labName;
    File currentLab;
    File iniFile;
    Properties pathProperties;
    String[] bases;
    String textEditorPref;
    public MainWindow() throws IOException {
        initComponents();
        //Set logo icon 
        ImageIcon logo = new ImageIcon("images/labtainer5-sm.png");
        this.setIconImage(logo.getImage());
        
        containerScrollPaneBar = ContainerScrollPane.getVerticalScrollBar();
        networkScrollPaneBar = NetworkScrollPane.getVerticalScrollBar();
        LabExistLabel.setVisible(false);
        
        labDataSaved = new LabData();    
        labDataCurrent = new LabData();   
        parseINI();
        getBaseImageDockerfiles();   
    }
    
    // checks out the ini file to set the labtainers path and also checks if we load a previous lab
    private void parseINI() throws IOException{
        // Load .ini file information
        try {
            iniFile = new File("/home/student/dev/Labtainers/UI/bin/mainUI.ini"); //location will need to be updated in final
            pathProperties  = new Properties();
            try{
                pathProperties.load(new FileInputStream(iniFile)); 
            } catch (FileNotFoundException ex) {
                //iniFile = new File("./mainUI.ini"); //location will need to be updated in final
                pathProperties.load(new FileInputStream(iniFile)); 
            } 
            //If the labtainers path has not been set in the config 
            if((pathProperties.getProperty("labtainerPath") == null) || (pathProperties.getProperty("labtainerPath").isEmpty())){
                System.out.println("No labtainer path set yet");
                
                // update the labtainerPath
                pathProperties.put("labtainerPath", System.getenv("LABTAINER_DIR"));
                FileOutputStream out = new FileOutputStream(iniFile);
                
                SimpleDateFormat formatter = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");
                Date date = new Date();
                pathProperties.store(out, "Updated: "+ formatter.format(date));
            } 
            
            labtainerPath = pathProperties.getProperty("labtainerPath");
            labsPath = new File(labtainerPath + File.separator + "labs");
            labChooser.setCurrentDirectory(labsPath);
            
            
            //if a lab has been loaded before then load that lab initially
            String iniPrevLab = pathProperties.getProperty("prevLab").trim();
            //System.out.println("iniPrevlab: "+iniPrevLab);
            File prevLab = new File(iniPrevLab);
            if(!iniPrevLab.isEmpty() && prevLab.isDirectory()){
                //System.out.println(prevLab+" is lab!");
                openLab(prevLab);
            }
            
            //check textEditor and load save its reference
            textEditorPref = pathProperties.getProperty("textEditor").trim();
            //if it's empty set it to 'vi'
            if(textEditorPref.isEmpty() || textEditorPref == null){
                textEditorPref = "vi";
                // update the textEditor
                pathProperties.put("textEditor", "vi");
                FileOutputStream out = new FileOutputStream(iniFile);
                
                SimpleDateFormat formatter = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");
                Date date = new Date();
                pathProperties.store(out, "Updated: "+ formatter.format(date));
            }
            
        } catch (FileNotFoundException ex) {
            System.out.println(ex);
        } catch (NullPointerException ex) {
            System.out.println(ex);
            //resetINIFile();
        }
    }

    // get list of base images ready for when player wants to make a new lab
    private void getBaseImageDockerfiles(){
        File dockerfileBasesPath = new File(labtainerPath + File.separator +"scripts"+ File.separator+"designer"+File.separator+"base_dockerfiles");
        File[] baseFiles = dockerfileBasesPath.listFiles(new FilenameFilter(){
            public boolean accept(File dockerfileBasesPath, String filename)
                {return filename.startsWith("Dockerfile.labtainer."); }
        } );
        
        bases = new String[baseFiles.length];
        for(int i = 0;i<baseFiles.length;i++){
            bases[i] = baseFiles[i].getName().split("Dockerfile.labtainer.")[1];
        }
        
//        String x;
//        for(String i : bases){
//            x = i;
//            System.out.println(x);
//        }
        
        //Set the base image combobox options for making new labs and adding containers
        for(String baseImage : bases){
            NewLabBaseImageComboBox.addItem(baseImage);
        }
        
        for(String baseImage : bases){
            ContainerAddDialogBaseImageCombobox.addItem(baseImage);
        }
        
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
        LabtainersDirDialog = new javax.swing.JDialog();
        jLabel15 = new javax.swing.JLabel();
        LabtainersDirTextfield = new javax.swing.JTextField();
        LabtainersDirCancelButton = new javax.swing.JButton();
        LabtainersDirConfirmButton = new javax.swing.JButton();
        pathValidLabel = new javax.swing.JLabel();
        TextEditorDialog = new javax.swing.JDialog();
        jLabel16 = new javax.swing.JLabel();
        TextEditorTextfield = new javax.swing.JTextField();
        TextEditorConfirmButton1 = new javax.swing.JButton();
        TextEditorCancelButton1 = new javax.swing.JButton();
        SaveAsDialog = new javax.swing.JDialog();
        SaveAsLabNameTextField = new javax.swing.JTextField();
        SaveAsErrorLabel = new javax.swing.JLabel();
        SaveAsCancelButton = new javax.swing.JButton();
        SaveAsConfirmButton = new javax.swing.JButton();
        Header = new javax.swing.JPanel();
        AssessmentButton = new javax.swing.JButton();
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
        MainMenuBar = new javax.swing.JMenuBar();
        FileMenuBar = new javax.swing.JMenu();
        NewLabMenuItem = new javax.swing.JMenuItem();
        jSeparator1 = new javax.swing.JPopupMenu.Separator();
        OpenLabMenuItem = new javax.swing.JMenuItem();
        jSeparator2 = new javax.swing.JPopupMenu.Separator();
        editLabtainersDir = new javax.swing.JMenuItem();
        editTextEditor = new javax.swing.JMenuItem();
        jSeparator3 = new javax.swing.JPopupMenu.Separator();
        SaveMenuItem = new javax.swing.JMenuItem();
        SaveAsMenuItem = new javax.swing.JMenuItem();
        jSeparator4 = new javax.swing.JPopupMenu.Separator();
        ExitMenuItem = new javax.swing.JMenuItem();

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

        labChooser.setCurrentDirectory(new java.io.File("/var/lib/snapd/void/C:/Users/Daniel Liao/Desktop/Labtainers/labs"));
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

        LabtainersDirDialog.setTitle("Edit LABTAINERS_DIRECTORY");
        LabtainersDirDialog.setMinimumSize(new java.awt.Dimension(400, 120));
        LabtainersDirDialog.setResizable(false);

        jLabel15.setText("Labtainers Dir:");

        LabtainersDirCancelButton.setText("Cancel");
        LabtainersDirCancelButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                LabtainersDirCancelButtonActionPerformed(evt);
            }
        });

        LabtainersDirConfirmButton.setText("Confirm");
        LabtainersDirConfirmButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                LabtainersDirConfirmButtonActionPerformed(evt);
            }
        });

        pathValidLabel.setText("Path not valid!");

        javax.swing.GroupLayout LabtainersDirDialogLayout = new javax.swing.GroupLayout(LabtainersDirDialog.getContentPane());
        LabtainersDirDialog.getContentPane().setLayout(LabtainersDirDialogLayout);
        LabtainersDirDialogLayout.setHorizontalGroup(
            LabtainersDirDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(LabtainersDirDialogLayout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jLabel15)
                .addGap(3, 3, 3)
                .addGroup(LabtainersDirDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(LabtainersDirDialogLayout.createSequentialGroup()
                        .addGap(0, 24, Short.MAX_VALUE)
                        .addComponent(pathValidLabel)
                        .addGap(18, 18, 18)
                        .addComponent(LabtainersDirConfirmButton)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(LabtainersDirCancelButton))
                    .addComponent(LabtainersDirTextfield))
                .addContainerGap())
        );
        LabtainersDirDialogLayout.setVerticalGroup(
            LabtainersDirDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(LabtainersDirDialogLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(LabtainersDirDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel15)
                    .addComponent(LabtainersDirTextfield, javax.swing.GroupLayout.PREFERRED_SIZE, 38, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(LabtainersDirDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(LabtainersDirCancelButton)
                    .addComponent(LabtainersDirConfirmButton)
                    .addComponent(pathValidLabel))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        TextEditorDialog.setMinimumSize(new java.awt.Dimension(400, 120));
        TextEditorDialog.setResizable(false);

        jLabel16.setText("Text Editor:");

        TextEditorConfirmButton1.setText("Confirm");
        TextEditorConfirmButton1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                TextEditorConfirmButton1ActionPerformed(evt);
            }
        });

        TextEditorCancelButton1.setText("Cancel");
        TextEditorCancelButton1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                TextEditorCancelButton1ActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout TextEditorDialogLayout = new javax.swing.GroupLayout(TextEditorDialog.getContentPane());
        TextEditorDialog.getContentPane().setLayout(TextEditorDialogLayout);
        TextEditorDialogLayout.setHorizontalGroup(
            TextEditorDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(TextEditorDialogLayout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jLabel16)
                .addGap(3, 3, 3)
                .addGroup(TextEditorDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(TextEditorDialogLayout.createSequentialGroup()
                        .addGap(0, 158, Short.MAX_VALUE)
                        .addComponent(TextEditorConfirmButton1)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(TextEditorCancelButton1))
                    .addComponent(TextEditorTextfield))
                .addContainerGap())
        );
        TextEditorDialogLayout.setVerticalGroup(
            TextEditorDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(TextEditorDialogLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(TextEditorDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel16)
                    .addComponent(TextEditorTextfield, javax.swing.GroupLayout.PREFERRED_SIZE, 38, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(TextEditorDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(TextEditorCancelButton1)
                    .addComponent(TextEditorConfirmButton1))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        SaveAsDialog.setTitle("Save As");
        SaveAsDialog.setMinimumSize(new java.awt.Dimension(400, 140));
        SaveAsDialog.setPreferredSize(new java.awt.Dimension(400, 140));

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
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addComponent(SaveAsErrorLabel)
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
            .addGroup(SaveAsDialogLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(SaveAsDialogLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
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
        addWindowListener(new java.awt.event.WindowAdapter() {
            public void windowClosing(java.awt.event.WindowEvent evt) {
                MainWindow.this.windowClosing(evt);
            }
        });

        AssessmentButton.setText("ASSESSMENT");
        AssessmentButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                AssessmentButtonActionPerformed(evt);
            }
        });

        LabnameLabel.setFont(new java.awt.Font("Arial Black", 0, 18)); // NOI18N
        LabnameLabel.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        LabnameLabel.setText("Lab:");

        javax.swing.GroupLayout HeaderLayout = new javax.swing.GroupLayout(Header);
        Header.setLayout(HeaderLayout);
        HeaderLayout.setHorizontalGroup(
            HeaderLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, HeaderLayout.createSequentialGroup()
                .addGap(20, 20, 20)
                .addComponent(LabnameLabel)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addComponent(AssessmentButton, javax.swing.GroupLayout.PREFERRED_SIZE, 160, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(35, 35, 35))
        );
        HeaderLayout.setVerticalGroup(
            HeaderLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(HeaderLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(HeaderLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(LabnameLabel)
                    .addComponent(AssessmentButton))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
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
                .addComponent(ContainerScrollPane, javax.swing.GroupLayout.DEFAULT_SIZE, 341, Short.MAX_VALUE)
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
                .addComponent(NetworkScrollPane, javax.swing.GroupLayout.DEFAULT_SIZE, 341, Short.MAX_VALUE)
                .addGap(10, 10, 10))
        );

        FileMenuBar.setText("File");

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

        editLabtainersDir.setText("Edit Labtainers Directory");
        editLabtainersDir.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                editLabtainersDirActionPerformed(evt);
            }
        });
        FileMenuBar.add(editLabtainersDir);

        editTextEditor.setText("Edit Text Editor");
        editTextEditor.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                editTextEditorActionPerformed(evt);
            }
        });
        FileMenuBar.add(editTextEditor);
        FileMenuBar.add(jSeparator3);

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

        ExitMenuItem.setText("Exit");
        ExitMenuItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                ExitMenuItemActionPerformed(evt);
            }
        });
        FileMenuBar.add(ExitMenuItem);

        MainMenuBar.add(FileMenuBar);

        setJMenuBar(MainMenuBar);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(Header, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                .addGap(20, 20, 20)
                .addComponent(ContainerPanel, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(NetworkPanel, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addGap(20, 20, 20))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addComponent(Header, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(ContainerPanel, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(NetworkPanel, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addGap(20, 20, 20))
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void AssessmentButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_AssessmentButtonActionPerformed
        // TODO add your handling code here:
    }//GEN-LAST:event_AssessmentButtonActionPerformed
    
   
    private void addContainerButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_addContainerButtonActionPerformed
        ContainerAddDialogNameTextfield.setText("");
        ContainerAddDialog.setVisible(true);
    }//GEN-LAST:event_addContainerButtonActionPerformed

    
    private void addNetworkButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_addNetworkButtonActionPerformed
        NetworkAddDialogGatewayTextfield.setText("");
        NetworkAddDialogIPRangeTextfield.setText("");
        NetworkAddDialogMacVLanExtSpinner.setValue(0);
        NetworkAddDialogMacVLanSpinner.setValue(0);
        NetworkAddDialogMaskTextfield.setText("");
        NetworkAddDialogNameTextfield.setText("");
        NetworkAddDialogTapRadioButton.setSelected(false);
        NetworkAddDialog.setVisible(true);
    }//GEN-LAST:event_addNetworkButtonActionPerformed


    private void ContainerAddDialogCreateButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_ContainerAddDialogCreateButtonActionPerformed
        addContainerPanel(null);
    }//GEN-LAST:event_ContainerAddDialogCreateButtonActionPerformed
    
    public int containerPanePanelLength = 0;
    private final JScrollBar containerScrollPaneBar;
    private void addContainerPanel(ContainerData data){
        //Resize the JPanel Holding all the ContainerObjPanels to fit another ContainerObjPanel 
        //(makes the scroll bar resize and should show all objects listed)
        containerPanePanelLength+=50;
        ContainerPanePanel.setPreferredSize(new Dimension(0,containerPanePanelLength));
        
        // Create the Container Obj Panel and add it
        ContainerObjPanel newContainer;
        if(data == null){ //if null then this is a new container being added
            newContainer = new ContainerObjPanel(this, ContainerAddDialogNameTextfield.getText());
            
            //Add the container into the labtainers directory
            addContainer(ContainerAddDialogNameTextfield.getText(), (String)ContainerAddDialogBaseImageCombobox.getSelectedItem());
        }
        else {
            newContainer = new ContainerObjPanel(this, data);
        }

        ContainerPanePanel.add(newContainer);
        
        // Redraw GUI with the new Panel
        ContainerPanePanel.revalidate();
        ContainerPanePanel.repaint(); 
        
        //Lower the Scroll Bar to show the newly added container (BUG[6/25/20]: still always off by a single panel)
        //System.out.println("Panel Length: "+containerPanePanelLength);
        //System.out.println("Max: "+(50+containerScrollPaneBar.getMaximum()));
        containerScrollPaneBar.setValue(50+containerScrollPaneBar.getMaximum());
        ContainerAddDialog.setVisible(false);
    }

    // Deletes the container in the lab directory structure by calling 'new_lab_setup.py -d containername'
    private void addContainer(String containerName, String baseImage){
        try{
                //call python new_lab_script: new_lab_setup.py -b basename
                String cmd = "./addContainer.sh "+labsPath+" "+labName+" "+containerName+" "+baseImage;
                System.out.println(cmd);
                Process pr = Runtime.getRuntime().exec(cmd);
            
                BufferedReader reader = new BufferedReader(new InputStreamReader(pr.getInputStream()));
                String line;
                while((line = reader.readLine()) != null){
                    System.out.println(line);
                }
                reader.close();
            } 
            catch (IOException e){
                System.out.println(e);
            }
    }
    
    private void NetworkAddDialogCreateButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_NetworkAddDialogCreateButtonActionPerformed
        //Create new networkData object here based on the field info and feeed it to teh funciton
        LabData.NetworkData newNetworkData = new LabData.NetworkData(
            NetworkAddDialogNameTextfield.getText().toUpperCase(),
            NetworkAddDialogMaskTextfield.getText(),
            NetworkAddDialogGatewayTextfield.getText(),
            (int)NetworkAddDialogMacVLanExtSpinner.getValue(),
            (int)NetworkAddDialogMacVLanSpinner.getValue(),
            NetworkAddDialogIPRangeTextfield.getText(),
            NetworkAddDialogTapRadioButton.isSelected());
        
        //Update the list of labs in the current UI data object
        labDataCurrent.getNetworks().add(newNetworkData);
        
        addNetworkPanel(newNetworkData);
    }//GEN-LAST:event_NetworkAddDialogCreateButtonActionPerformed
   
    //[BUG: 6/25/2020] Not sure Why but the network obj panel needs to be 1 px taller than the container panel to be the same size
    public int networkPanePanelLength = 0;
    private JScrollBar networkScrollPaneBar;
    private void addNetworkPanel(NetworkData data){
        //Resize the JPanel Holding all the NetworkObjPanels to fit another NetworkObjPanel 
        //(makes the scroll bar resize and should show all objects listed)
        networkPanePanelLength+=51;
        NetworkPanePanel.setPreferredSize(new Dimension(0,networkPanePanelLength));
        
        // Create the Network Obj Panel and add it
        NetworkPanePanel.add(new NetworkObjPanel(this, data));
        
        // Redraw GUI with the new Panel
        NetworkPanePanel.revalidate();
        NetworkPanePanel.repaint(); 
        
        //Lower the Scroll Bar to show the newly added container (BUG[6/25/20]: still always off by a single panel)
        //System.out.println("Panel Length: "+networkPanePanelLength);
        //System.out.println("Max: "+(51+networkScrollPaneBar.getMaximum()));
        networkScrollPaneBar.setValue(networkScrollPaneBar.getMaximum());
        NetworkAddDialog.setVisible(false);
    }    
    
    private void OpenLabMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_OpenLabMenuItemActionPerformed
            int returnVal = labChooser.showOpenDialog(this);
            if (returnVal == JFileChooser.APPROVE_OPTION) {
                File lab = labChooser.getSelectedFile();
                openLab(lab);
            } 
            else {
                System.out.println("File access cancelled by user.");
            }
    }//GEN-LAST:event_OpenLabMenuItemActionPerformed
    
private void openLab(File lab){
    currentLab = lab;
    labName = lab.toString().substring(lab.toString().lastIndexOf(File.separator)+1);
           
    labDataSaved = new LabData(lab, labName); //initialize all data for the lab
    labDataCurrent = new LabData(lab, labName); //initialize all data for the lab
     
    
    // Visual load of lab
    resetWindow();
    loadLab();
    System.out.println(labName);
    labDataCurrent.printData();    
    System.out.println();
        System.out.println();
            System.out.println();


}    

    private void NetworkAddDialogCancelButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_NetworkAddDialogCancelButtonActionPerformed
        NetworkAddDialog.setVisible(false);
    }//GEN-LAST:event_NetworkAddDialogCancelButtonActionPerformed

    private void windowClosing(java.awt.event.WindowEvent evt) {//GEN-FIRST:event_windowClosing
        exitProgram();
    }//GEN-LAST:event_windowClosing
    
    // When exiting the program save the the current lab into the ini file so that it opens immediately when returning to the program
    private void exitProgram(){
        //Write the current lab to the ini so that when the app opens again it opens to this lab
        FileOutputStream out = null;
        try {
            out = new FileOutputStream(iniFile);
            if(out != null){
                //String tmp = File.toString(currentLab);
                pathProperties.put("prevLab", currentLab.getPath());

                SimpleDateFormat formatter = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");
                Date date = new Date();

                pathProperties.store(out, "Updated: "+ formatter.format(date));
            }
            
        } 
        catch (FileNotFoundException ex) { System.out.println(ex);} 
        catch (IOException ex) { System.out.println(ex);} 
        catch (NullPointerException ex) {
            System.out.println(ex);
            resetINIFile();
        }
        
        finally {
            try { if(out != null){out.close();}} 
            catch (IOException ex) { System.out.println(ex);}
        }
    }
    // Code taken from Beginners Book: https://beginnersbook.com/2014/05/how-to-copy-a-file-to-another-file-in-java/
    private void resetINIFile(){
        FileInputStream instream = null;
	FileOutputStream outstream = null;
 
    	try{
    	    File infile = new File("/home/student/dev/Labtainers/UI/bin/mainUI.ini.backup"); //location will need to be updated in final;
    	    File outfile = iniFile;
 
    	    instream = new FileInputStream(infile);
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
    
    private void NewLabMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_NewLabMenuItemActionPerformed
        NewLabNameTextfield.setText("");
        NewLabDialog.setVisible(true);
        NewLabNameTextfield.requestFocusInWindow();
    }//GEN-LAST:event_NewLabMenuItemActionPerformed

    private void NewLabCreateButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_NewLabCreateButtonActionPerformed
        createNewLab();
    }//GEN-LAST:event_NewLabCreateButtonActionPerformed

    private void createNewLab(){
        LabExistLabel.setVisible(false);
        
        //mkdir newlab (in labs dir if )
        String newLabName = NewLabNameTextfield.getText();
        if(!Arrays.asList(labsPath.list()).contains(newLabName)){ // If lab doesn't exist
            try{
                LabExistLabel.setVisible(false);
                NewLabDialog.revalidate();
                System.out.println("made new lab");
                //call python new_lab_script: new_lab_setup.py -b basename              
                String cmd = "./callNewLab.sh "+labsPath+" "+newLabName+" "+NewLabBaseImageComboBox.getSelectedItem();
                System.out.println(cmd);
                Process pr = Runtime.getRuntime().exec(cmd);
            
                BufferedReader reader = new BufferedReader(new InputStreamReader(pr.getInputStream()));
                String line;
                while((line = reader.readLine()) != null){
                    System.out.println(line);
                }
                reader.close();
                NewLabDialog.setVisible(false);
                
                //open the new lab
                openLab(new File(labsPath+File.separator+newLabName));
            } 
            catch (IOException e){
                System.out.println(e);
            }
           
        }
        else{
            System.out.println("Lab already exists. Make the lab with a different name other than:");
            LabExistLabel.setVisible(true);
            NewLabDialog.revalidate();
            int labCount = 1;
            for(String lab : labsPath.list()){
                System.out.print(lab + ", ");
                if(labCount % 5 == 0){
                    System.out.println();
                }
                labCount++;
            }
        }
    }
    
    private void NewLabCancelButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_NewLabCancelButtonActionPerformed
        NewLabDialog.setVisible(false);
    }//GEN-LAST:event_NewLabCancelButtonActionPerformed

    private void editLabtainersDirActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_editLabtainersDirActionPerformed
        LabtainersDirTextfield.setText(labtainerPath);
        pathValidLabel.setVisible(false);
        LabtainersDirDialog.setVisible(true);
    }//GEN-LAST:event_editLabtainersDirActionPerformed

    private void LabtainersDirCancelButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_LabtainersDirCancelButtonActionPerformed
        LabtainersDirDialog.setVisible(false);
    }//GEN-LAST:event_LabtainersDirCancelButtonActionPerformed

    private void LabtainersDirConfirmButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_LabtainersDirConfirmButtonActionPerformed
        try {
            setLabtainersDir();
        } catch (IOException ex) {
            Logger.getLogger(MainWindow.class.getName()).log(Level.SEVERE, null, ex);
        }
    }//GEN-LAST:event_LabtainersDirConfirmButtonActionPerformed

    private void SaveMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_SaveMenuItemActionPerformed
        try {
            saveLab();
        } catch (FileNotFoundException ex) {
            Logger.getLogger(MainWindow.class.getName()).log(Level.SEVERE, null, ex);
        }
    }//GEN-LAST:event_SaveMenuItemActionPerformed
    
    private void saveLab() throws FileNotFoundException{
        //Get path to start.config
        String startConfigPath = currentLab.getPath()+File.separator+"config"+File.separator+"start.config";
        PrintWriter writer = new PrintWriter(startConfigPath);
        String startConfigText = ""; 
         
        // Write Global Params
        for(String line : labDataCurrent.getGlobals()){
            startConfigText += line+"\n";
        }

        // Cycle through network objects and write
        Component[] networks = NetworkPanePanel.getComponents();
        for(Component network : networks){
            NetworkData data = ((NetworkObjPanel)network).getConfigData();
            startConfigText += "NETWORK "+data.name+"\n";
            startConfigText += "     MASK "+data.mask+"\n";
            startConfigText += "     GATEWAY "+data.gateway+"\n";
            
            if(data.macvlan > 0){
                startConfigText += "     MACVLAN "+data.macvlan+"\n";
            }
            if(data.macvlan_ext > 0){
                startConfigText += "     MACVLAN_EXT" +data.macvlan_ext+"\n";
            }
            
            if(!data.ip_range.isEmpty()){
                startConfigText += "     IP_RANGE "+data.ip_range+"\n";
            }        

            if(data.tap){
                startConfigText += "     TAP YES"+"\n";
            }
            for(String unknownParam : data.unknownNetworkParams){
                startConfigText += "     "+unknownParam+"\n";
            }
        }
        
        // Cycle through container objects and write 
        Component[] containers = ContainerPanePanel.getComponents();
        for(Component container : containers){
            ContainerData data = ((ContainerObjPanel)container).getConfigData(); 
            startConfigText += "CONTAINER "+data.name+"\n";
            startConfigText += "     USER "+data.user+"\n";
            if(data.script.isEmpty()){
               startConfigText += "     SCRIPT NONE\n";
            }
            else{
               startConfigText += "     SCRIPT "+data.script+"\n"; 
            }
                
            if(data.x11){
                startConfigText += "     X11 YES\n"; 
            }
            else{
                startConfigText += "     X11 NO\n";
            }
            // Not default
            if(data.terminal_count != 1)
                startConfigText += "     TERMINALS "+data.terminal_count+"\n";
            if(!data.terminal_group.isEmpty())
                startConfigText += "     TERMINAL_GROUP "+data.terminal_group+"\n";
            if(!data.xterm_title.isEmpty())
                startConfigText += "     XTERM "+data.xterm_title+" "+data.xterm_script+"\n";
            if(!data.password.isEmpty())
                startConfigText += "     PASSWORD "+data.password+"\n";
            for(LabData.ContainerAddHostSubData addHost : data.listOfContainerAddHost){
                if(addHost.type.equals("network"))
                    startConfigText += "     ADD-HOST "+addHost.add_host_network+"\n";
                else if(addHost.type.equals("ip"))
                    startConfigText += "     ADD-HOST "+addHost.add_host_host+":"+addHost.add_host_ip+"\n";    
            }
            for(LabData.ContainerNetworkSubData network : data.listOfContainerNetworks){
                    startConfigText += "     "+network.network_name+" "+network.network_ipaddress+"\n";  
            }
            if(data.clone > 0){
                startConfigText += "     CLONE "+data.clone+"\n";
            }
            if(!data.lab_gateway.isEmpty()){
                startConfigText += "     LAB_GATEWAY "+data.lab_gateway+"\n";
            }
            if(data.no_gw){
                startConfigText += "     NO_GW YES\n";
            }
            if(!data.base_registry.isEmpty()){
                startConfigText += "     BASE_REGISTRY "+data.base_registry+"\n";
            }
            if(!data.thumb_volume.isEmpty()){
                startConfigText += "     THUMB_VOLUME "+data.thumb_volume+"\n";
            }
            if(!data.thumb_command.isEmpty()){
                startConfigText += "     THUMB_COMMAND "+data.thumb_command+"\n";
            }
            if(!data.thumb_stop.isEmpty()){
                startConfigText += "     THUMB_STOP "+data.thumb_stop+"\n";
            }
            if(!data.publish.isEmpty()){
                startConfigText += "     PUBLISH "+data.publish+"\n";
            }
            if(data.hide){
                startConfigText += "     HIDE YES\n";
            }
            if(data.no_privilege){
                startConfigText += "     NO_PRIVILEGE YES\n";
            }
            if(data.no_pull){
                startConfigText += "     NO_PULL YES\n";
            }
            if(data.mystuff){
                startConfigText += "     MYSTUFF YES\n";
            }
            if(data.tap){
                startConfigText += "     TAP YES\n";
            }
            if(!data.mount1.isEmpty() && !data.mount2.isEmpty()){
                startConfigText += "     MOUNT "+data.mount1+":"+data.mount2+"\n";
            }
            
        }
        
        //Write to File
        writer.print(startConfigText);
        writer.close();
    }
    
    private void SaveAsMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_SaveAsMenuItemActionPerformed
        SaveAsLabNameTextField.setText("");
        SaveAsErrorLabel.setVisible(false);
        SaveAsDialog.setVisible(true);
    }//GEN-LAST:event_SaveAsMenuItemActionPerformed
    
    private void editTextEditorActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_editTextEditorActionPerformed
        TextEditorTextfield.setText(textEditorPref);
        TextEditorDialog.setVisible(true);
    }//GEN-LAST:event_editTextEditorActionPerformed

    private void TextEditorConfirmButton1ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_TextEditorConfirmButton1ActionPerformed
        try {
            setTextEditor();
        } catch (IOException ex) {
            Logger.getLogger(MainWindow.class.getName()).log(Level.SEVERE, null, ex);
        }
    }//GEN-LAST:event_TextEditorConfirmButton1ActionPerformed

    private void TextEditorCancelButton1ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_TextEditorCancelButton1ActionPerformed
        TextEditorDialog.setVisible(false);
    }//GEN-LAST:event_TextEditorCancelButton1ActionPerformed

    private void ExitMenuItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_ExitMenuItemActionPerformed
        exitProgram();
        System.exit(0);
    }//GEN-LAST:event_ExitMenuItemActionPerformed

    private void SaveAsCancelButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_SaveAsCancelButtonActionPerformed
        SaveAsDialog.setVisible(false);
    }//GEN-LAST:event_SaveAsCancelButtonActionPerformed

    private void SaveAsConfirmButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_SaveAsConfirmButtonActionPerformed
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
    }//GEN-LAST:event_SaveAsConfirmButtonActionPerformed
    
    private void saveAs(String newLabName){
        // Call Clone Script, feeding in the new lab name
        try{
            //call python new_lab_script: new_lab_setup.py -c newLabName
            String cmd = "./cloneLab.sh "+labsPath+" "+labName+" "+newLabName;
            System.out.println(cmd);
            Process pr = Runtime.getRuntime().exec(cmd);

            BufferedReader reader = new BufferedReader(new InputStreamReader(pr.getInputStream()));
            String line;
            while((line = reader.readLine()) != null){
                System.out.println(line);
            }
            reader.close();
        
        //Rename to current lab and set the path to the new lab
        this.labName = newLabName;
        LabnameLabel.setText("Lab: "+this.labName);
        this.currentLab = new File(labsPath+File.separator+this.labName);
        this.labDataCurrent.setName(this.labName);
        this.labDataCurrent.setPath(this.currentLab);
        
        
        //Write the current state to the new lab's start.config
        //saveLab();
        
        SaveAsDialog.setVisible(false);
        } 
        catch (IOException e){
            System.out.println(e);
        }
    }
    
    
    private void setLabtainersDir() throws IOException{
            String newLabtainersPath = LabtainersDirTextfield.getText();
            
            //check if labtainers path exist
            if(new File(newLabtainersPath).isDirectory()){
                pathValidLabel.setVisible(false);
                // update the labtainerPath property
                pathProperties  = new Properties();
                pathProperties.load(new FileInputStream(iniFile)); 
                pathProperties.put("labtainerPath", newLabtainersPath);

                //write update to the ini File
                SimpleDateFormat formatter = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");
                Date date = new Date();
                FileOutputStream out = new FileOutputStream(iniFile);
                pathProperties.store(out, "Updated: "+ formatter.format(date));


                //update UI state 
                labtainerPath = pathProperties.getProperty("labtainerPath");
                labsPath = new File(labtainerPath + File.separator + "labs");
                labChooser.setCurrentDirectory(labsPath);   
                
                LabtainersDirDialog.setVisible(false);
            }
            else{
                pathValidLabel.setVisible(true);
            }  
    }
    
    private void setTextEditor() throws FileNotFoundException, IOException{
        String newTextEditor = TextEditorTextfield.getText(); 
        
        //*Include validation check to see it the file editor is proper program 
        
        // update the labtainerPath property
        pathProperties  = new Properties();
        pathProperties.load(new FileInputStream(iniFile)); 
        pathProperties.put("textEditor", newTextEditor);

        //write update to the ini File
        SimpleDateFormat formatter = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");
        Date date = new Date();
        FileOutputStream out = new FileOutputStream(iniFile);
        pathProperties.store(out, "Updated: "+ formatter.format(date));


        //update UI state 
        textEditorPref = pathProperties.getProperty("textEditor"); 

        TextEditorDialog.setVisible(false);
    }
    
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
    
    // Load the data visually
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
    private javax.swing.JButton AssessmentButton;
    private javax.swing.JDialog ContainerAddDialog;
    private javax.swing.JComboBox<String> ContainerAddDialogBaseImageCombobox;
    private javax.swing.JButton ContainerAddDialogCancelButton;
    private javax.swing.JButton ContainerAddDialogCreateButton;
    private javax.swing.JTextField ContainerAddDialogNameTextfield;
    private javax.swing.JPanel ContainerPanePanel;
    private javax.swing.JPanel ContainerPanel;
    private javax.swing.JScrollPane ContainerScrollPane;
    private javax.swing.JMenuItem ExitMenuItem;
    private javax.swing.JMenu FileMenuBar;
    private javax.swing.JPanel Header;
    private javax.swing.JLabel LabExistLabel;
    private javax.swing.JLabel LabnameLabel;
    private javax.swing.JButton LabtainersDirCancelButton;
    private javax.swing.JButton LabtainersDirConfirmButton;
    private javax.swing.JDialog LabtainersDirDialog;
    private javax.swing.JTextField LabtainersDirTextfield;
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
    private javax.swing.JButton SaveAsCancelButton;
    private javax.swing.JButton SaveAsConfirmButton;
    private javax.swing.JDialog SaveAsDialog;
    private javax.swing.JLabel SaveAsErrorLabel;
    private javax.swing.JTextField SaveAsLabNameTextField;
    private javax.swing.JMenuItem SaveAsMenuItem;
    private javax.swing.JMenuItem SaveMenuItem;
    private javax.swing.JButton TextEditorCancelButton1;
    private javax.swing.JButton TextEditorConfirmButton1;
    private javax.swing.JDialog TextEditorDialog;
    private javax.swing.JTextField TextEditorTextfield;
    private javax.swing.JButton addContainerButton;
    private javax.swing.JButton addNetworkButton;
    private javax.swing.JMenuItem editLabtainersDir;
    private javax.swing.JMenuItem editTextEditor;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel10;
    private javax.swing.JLabel jLabel11;
    private javax.swing.JLabel jLabel12;
    private javax.swing.JLabel jLabel13;
    private javax.swing.JLabel jLabel14;
    private javax.swing.JLabel jLabel15;
    private javax.swing.JLabel jLabel16;
    private javax.swing.JLabel jLabel2;
    private javax.swing.JLabel jLabel3;
    private javax.swing.JLabel jLabel4;
    private javax.swing.JLabel jLabel5;
    private javax.swing.JLabel jLabel6;
    private javax.swing.JLabel jLabel7;
    private javax.swing.JLabel jLabel8;
    private javax.swing.JLabel jLabel9;
    private javax.swing.JPopupMenu.Separator jSeparator1;
    private javax.swing.JPopupMenu.Separator jSeparator2;
    private javax.swing.JPopupMenu.Separator jSeparator3;
    private javax.swing.JPopupMenu.Separator jSeparator4;
    private javax.swing.JFileChooser labChooser;
    private javax.swing.JLabel pathValidLabel;
    // End of variables declaration//GEN-END:variables
}
