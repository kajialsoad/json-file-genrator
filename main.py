#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gmail OAuth Client JSON Generator
স্বয়ংক্রিয় জিমেইল OAuth ক্লায়েন্ট জেনারেটর

এই অ্যাপ্লিকেশনটি ব্যবহারকারীর কাছ থেকে ইমেল এবং পাসওয়ার্ড নিয়ে
স্বয়ংক্রিয়ভাবে Google Cloud Console এ OAuth ক্লায়েন্ট তৈরি করে
এবং JSON ফাইল হিসেবে আউটপুট দেয়।
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import threading
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class GmailOAuthGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Gmail OAuth Client JSON Generator")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Variables
        self.selected_file = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Ready to start...")
        
        # Create output directory
        self.output_dir = "output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        # Log display variables
        self.log_text = None
            
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        self.root.title("Gmail OAuth Client JSON Generator")
        self.root.geometry("900x800")
        self.root.resizable(True, True)
        self.root.configure(bg='#f8f9fa')
        
        # Set minimum window size
        self.root.minsize(800, 700)
        
        # Create main canvas and scrollbar for scrollable content
        canvas = tk.Canvas(self.root, bg='#f8f9fa', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=2)
        scrollbar.pack(side="right", fill="y")
        
        # Add mouse wheel scrolling support
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Use scrollable_frame as main container instead of self.root
        main_container = scrollable_frame
        
        # Configure modern style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles with professional colors
        style.configure('Title.TLabel', font=('Segoe UI', 20, 'bold'), 
                       foreground='#1a365d', background='#f8f9fa')
        style.configure('Heading.TLabel', font=('Segoe UI', 13, 'bold'), 
                       foreground='#2d3748', background='#ffffff')
        style.configure('Modern.TButton', font=('Segoe UI', 11, 'bold'),
                       padding=(25, 12))
        style.configure('Browse.TButton', font=('Segoe UI', 10),
                       padding=(12, 8))
        
        # Configure progress bar style
        style.configure('Professional.Horizontal.TProgressbar',
                       background='#4299e1',
                       troughcolor='#e2e8f0',
                       borderwidth=0,
                       lightcolor='#4299e1',
                       darkcolor='#4299e1')
        
        # Main container with modern styling (now using scrollable_frame)
        main_container.configure(bg='#f8f9fa')
        
        # Create content frame with enhanced padding
        content_frame = tk.Frame(main_container, bg='#f8f9fa')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=35)
        
        # Header section with professional gradient-like effect
        header_frame = tk.Frame(content_frame, bg='#ffffff', relief=tk.FLAT, bd=0)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Add subtle shadow effect with multiple frames
        shadow_frame = tk.Frame(content_frame, bg='#e2e8f0', height=2)
        shadow_frame.pack(fill=tk.X, pady=(0, 28))
        
        # Professional title with enhanced styling
        title_label = tk.Label(header_frame, text="Gmail OAuth Client JSON Generator", 
                              font=('Segoe UI', 22, 'bold'), fg='#1a365d', bg='#ffffff')
        title_label.pack(pady=25)
        
        # Subtitle for better hierarchy
        subtitle_label = tk.Label(header_frame, text="Automated OAuth Client JSON File Generator", 
                                 font=('Segoe UI', 11), fg='#4a5568', bg='#ffffff')
        subtitle_label.pack(pady=(0, 20))
        
        # File selection section with enhanced card design
        file_section = tk.LabelFrame(content_frame, text="📁 File Selection", 
                                   font=('Segoe UI', 13, 'bold'), fg='#2d3748',
                                   bg='#ffffff', relief=tk.FLAT, bd=0, padx=25, pady=20)
        file_section.pack(fill=tk.X, pady=(0, 25))
        
        # Add card shadow effect
        file_section.configure(highlightbackground='#e2e8f0', highlightthickness=1)
        
        accounts_label = tk.Label(file_section, text="Select Account File:", 
                                 font=('Segoe UI', 11, 'bold'), fg='#2d3748', bg='#ffffff')
        accounts_label.grid(row=0, column=0, sticky=tk.W, pady=(8, 15))
        
        file_frame = tk.Frame(file_section, bg='#ffffff')
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        file_section.columnconfigure(0, weight=1)
        
        # Enhanced file entry with better styling
        file_entry = tk.Entry(file_frame, textvariable=self.selected_file, 
                             font=('Segoe UI', 11), width=55, relief=tk.FLAT, bd=0, 
                             state="readonly", bg='#f7fafc', fg='#2d3748',
                             highlightbackground='#cbd5e0', highlightthickness=1)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15), ipady=8)
        
        # Enhanced browse button
        browse_button = tk.Button(file_frame, text="📂 Browse", command=self.browse_file,
                                 font=('Segoe UI', 10, 'bold'), bg='#4299e1', fg='white',
                                 relief=tk.FLAT, padx=20, pady=10, cursor='hand2',
                                 activebackground='#3182ce', activeforeground='white')
        browse_button.pack(side=tk.RIGHT)
        
        # Single Account section with enhanced card design
        single_section = tk.LabelFrame(content_frame, text="👤 Single Account Generator", 
                                     font=('Segoe UI', 13, 'bold'), fg='#2d3748',
                                     bg='#ffffff', relief=tk.FLAT, bd=0, padx=25, pady=20)
        single_section.pack(fill=tk.X, pady=(0, 25))
        
        # Add card shadow effect
        single_section.configure(highlightbackground='#e2e8f0', highlightthickness=1)
        
        # Variables for single account inputs
        self.single_email = tk.StringVar()
        self.single_password = tk.StringVar()
        
        # Email input
        email_label = tk.Label(single_section, text="Email Address:", 
                              font=('Segoe UI', 11, 'bold'), fg='#2d3748', bg='#ffffff')
        email_label.grid(row=0, column=0, sticky=tk.W, pady=(8, 5), padx=(0, 10))
        
        email_entry = tk.Entry(single_section, textvariable=self.single_email, 
                              font=('Segoe UI', 11), width=40, relief=tk.FLAT, bd=0, 
                              bg='#f7fafc', fg='#2d3748',
                              highlightbackground='#cbd5e0', highlightthickness=1)
        email_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(8, 5), padx=(0, 15), ipady=8)
        
        # Password input
        password_label = tk.Label(single_section, text="Password:", 
                                 font=('Segoe UI', 11, 'bold'), fg='#2d3748', bg='#ffffff')
        password_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 15), padx=(0, 10))
        
        password_entry = tk.Entry(single_section, textvariable=self.single_password, 
                                 font=('Segoe UI', 11), width=40, relief=tk.FLAT, bd=0, 
                                 bg='#f7fafc', fg='#2d3748', show='*',
                                 highlightbackground='#cbd5e0', highlightthickness=1)
        password_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(5, 15), padx=(0, 15), ipady=8)
        
        # Configure grid weights
        single_section.columnconfigure(1, weight=1)
        
        # Generate button for single account
        single_generate_btn = tk.Button(single_section, text="🚀 Generate Single JSON", 
                                       command=self.start_single_generation,
                                       font=('Segoe UI', 11, 'bold'), bg='#9f7aea', fg='white',
                                       relief=tk.FLAT, bd=0, padx=25, pady=12, cursor='hand2',
                                       activebackground='#805ad5', activeforeground='white')
        single_generate_btn.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        # Store reference to single generate button
        self.single_generate_btn = single_generate_btn
        
        # Instructions section with enhanced card design
        instructions_section = tk.LabelFrame(content_frame, text="📋 Instructions", 
                                           font=('Segoe UI', 13, 'bold'), fg='#2d3748',
                                           bg='#ffffff', relief=tk.FLAT, bd=0, padx=25, pady=20)
        instructions_section.pack(fill=tk.X, pady=(0, 25))
        
        # Add card shadow effect
        instructions_section.configure(highlightbackground='#e2e8f0', highlightthickness=1)
        
        instructions_text = (
            "1. Add accounts in email:password format (one per line) in the selected file\n"
            "2. Click the 'Generate OAuth Credentials' button to start the process\n"
            "3. Complete 2FA verification when prompted during automation\n"
            "4. Generated JSON files will be saved in the output folder"
        )
        
        # Enhanced instructions display with better styling
        instructions_display = tk.Text(instructions_section, height=4, width=75, wrap=tk.WORD,
                                     font=('Segoe UI', 10), bg='#f7fafc', relief=tk.FLAT, bd=0,
                                     fg='#4a5568', highlightbackground='#cbd5e0', highlightthickness=1,
                                     padx=15, pady=10, selectbackground='#bee3f8')
        instructions_display.insert(tk.END, instructions_text)
        instructions_display.config(state=tk.DISABLED)
        instructions_display.pack(fill=tk.X, pady=(10, 5))
        
        # Progress section with enhanced card design
        progress_section = tk.LabelFrame(content_frame, text="⚡ Progress Status", 
                                       font=('Segoe UI', 13, 'bold'), fg='#2d3748',
                                       bg='#ffffff', relief=tk.FLAT, bd=0, padx=25, pady=20)
        progress_section.pack(fill=tk.X, pady=(0, 25))
        
        # Add card shadow effect
        progress_section.configure(highlightbackground='#e2e8f0', highlightthickness=1)
        
        # Enhanced status display with better styling
        status_display = tk.Label(progress_section, textvariable=self.status_var,
                                   font=('Segoe UI', 11), fg='#2d3748', bg='#ffffff',
                                   wraplength=600, justify=tk.LEFT)
        status_display.pack(pady=(10, 15))
        
        # Professional progress bar with custom styling
        self.progress_bar = ttk.Progressbar(progress_section, variable=self.progress_var,
                                          maximum=100, length=600, 
                                          style='Professional.Horizontal.TProgressbar')
        self.progress_bar.pack(pady=(0, 15))
        
        # Actions section with professional card design
        actions_section = tk.LabelFrame(content_frame, text="🎯 Actions", 
                                       font=('Segoe UI', 13, 'bold'), fg='#2d3748',
                                       bg='#ffffff', relief=tk.FLAT, bd=0, padx=25, pady=25)
        actions_section.pack(fill=tk.X, pady=(0, 30))
        
        # Add card shadow effect
        actions_section.configure(highlightbackground='#e2e8f0', highlightthickness=1)
        
        # Create a centered container for buttons with professional spacing
        button_container = tk.Frame(actions_section, bg='#ffffff')
        button_container.pack(pady=(15, 20))
        
        # Generate JSON Files button with professional styling
        self.generate_btn = tk.Button(button_container, text="🚀 Generate JSON Files", 
                                        command=self.start_generation,
                                        font=('Segoe UI', 12, 'bold'), bg='#48bb78', fg='white',
                                        relief=tk.FLAT, bd=0, padx=35, pady=15, cursor='hand2',
                                        activebackground='#38a169', activeforeground='white')
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 25))
        
        # Open Output Folder button with professional styling
        open_output_btn = tk.Button(button_container, text="📁 Open Output Folder", 
                                 command=self.open_output_folder,
                                 font=('Segoe UI', 12, 'bold'), bg='#ed8936', fg='white',
                                 relief=tk.FLAT, bd=0, padx=30, pady=15, cursor='hand2',
                                 activebackground='#dd6b20', activeforeground='white')
        open_output_btn.pack(side=tk.LEFT)
        
        # Add professional hover effects with smooth transitions
        self.add_hover_effects(browse_button, '#3182ce', '#4299e1')
        self.add_hover_effects(self.generate_btn, '#38a169', '#48bb78')
        self.add_hover_effects(open_output_btn, '#dd6b20', '#ed8936')
        self.add_hover_effects(self.single_generate_btn, '#805ad5', '#9f7aea')
        
        # Log Display section with enhanced card design
        log_section = tk.LabelFrame(content_frame, text="📋 Process Log", 
                                   font=('Segoe UI', 13, 'bold'), fg='#2d3748',
                                   bg='#ffffff', relief=tk.FLAT, bd=0, padx=25, pady=20)
        log_section.pack(fill=tk.BOTH, expand=True, pady=(0, 25))
        
        # Add card shadow effect
        log_section.configure(highlightbackground='#e2e8f0', highlightthickness=1)
        
        # Create frame for log text and scrollbar
        log_frame = tk.Frame(log_section, bg='#ffffff')
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 15))
        
        # Create scrollable text widget for logs
        self.log_text = tk.Text(log_frame, height=12, wrap=tk.WORD,
                               font=('Consolas', 10), bg='#1a202c', fg='#e2e8f0',
                               relief=tk.FLAT, bd=0, padx=15, pady=10,
                               selectbackground='#4a5568', insertbackground='#e2e8f0')
        
        # Create scrollbar for log text
        log_scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        # Pack log text and scrollbar
        self.log_text.pack(side="left", fill="both", expand=True)
        log_scrollbar.pack(side="right", fill="y")
        
        # Clear log button
        clear_log_btn = tk.Button(log_section, text="🗑️ Clear Log", 
                                 command=self.clear_log,
                                 font=('Segoe UI', 10, 'bold'), bg='#e53e3e', fg='white',
                                 relief=tk.FLAT, bd=0, padx=20, pady=8, cursor='hand2',
                                 activebackground='#c53030', activeforeground='white')
        clear_log_btn.pack(pady=(0, 10))
        
        # Add hover effect to clear button
        self.add_hover_effects(clear_log_btn, '#c53030', '#e53e3e')
        
        # Initialize log with welcome message
        self.log_message("📋 Gmail OAuth Client JSON Generator - Ready to start!", "INFO")
        self.log_message("💡 Select a file or enter single account details to begin.", "INFO")
        
        # Add bottom spacing for better visual balance
        bottom_spacer = tk.Frame(content_frame, bg='#f8f9fa', height=30)
        bottom_spacer.pack(fill=tk.X)
        
    def add_hover_effects(self, button, hover_color, normal_color):
        """Add hover effects to buttons"""
        def on_enter(e):
            button.config(bg=hover_color)
            
        def on_leave(e):
            button.config(bg=normal_color)
            
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
    def log_message(self, message, level="INFO"):
        """Add a message to the log display with timestamp"""
        if self.log_text is None:
            return
            
        timestamp = time.strftime("%H:%M:%S")
        
        # Color coding for different log levels
        colors = {
            "INFO": "#4299e1",    # Blue
            "SUCCESS": "#48bb78",  # Green
            "WARNING": "#ed8936",  # Orange
            "ERROR": "#e53e3e",    # Red
            "STEP": "#9f7aea"      # Purple
        }
        
        color = colors.get(level, "#e2e8f0")  # Default white
        
        # Configure text tags for colors
        self.log_text.tag_configure(level, foreground=color)
        
        # Insert the log message
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        self.log_text.insert(tk.END, log_entry, level)
        
        # Auto-scroll to bottom
        self.log_text.see(tk.END)
        
        # Update the UI
        self.root.update_idletasks()
        
    def clear_log(self):
        """Clear the log display"""
        if self.log_text is not None:
            self.log_text.delete(1.0, tk.END)
            self.log_message("📋 Log cleared - Ready for new operations!", "INFO")
        
    def browse_file(self):
        """Browse and select account file"""
        self.log_message("📂 Opening file browser...", "STEP")
        filename = filedialog.askopenfilename(
            title="Select Account File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.selected_file.set(filename)
            self.log_message(f"✅ File selected: {os.path.basename(filename)}", "SUCCESS")
        else:
            self.log_message("❌ No file selected", "WARNING")
            
    def open_output_folder(self):
        """Open output folder"""
        if os.path.exists(self.output_dir):
            os.startfile(self.output_dir)
        else:
            messagebox.showwarning("Warning", "Output folder not found!")
            
    def start_generation(self):
        """Start OAuth client generation process"""
        if not self.selected_file.get():
            self.log_message("❌ No file selected! Please select a file first.", "ERROR")
            messagebox.showerror("Error", "Please select a file first!")
            return
            
        self.log_message("🚀 Starting batch OAuth client generation...", "STEP")
        self.log_message(f"📄 Processing file: {os.path.basename(self.selected_file.get())}", "INFO")
        
        # Disable generate button
        self.generate_btn.config(state="disabled")
        
        # Start generation in separate thread
        thread = threading.Thread(target=self.generate_oauth_clients)
        thread.daemon = True
        thread.start()
        
    def start_single_generation(self):
        """Start single account OAuth client generation process"""
        email = self.single_email.get().strip()
        password = self.single_password.get().strip()
        
        self.log_message("🔍 Validating single account input...", "STEP")
        
        # Validation
        if not email:
            self.log_message("❌ Email address is required!", "ERROR")
            messagebox.showerror("Error", "Please enter an email address!")
            return
            
        if not password:
            self.log_message("❌ Password is required!", "ERROR")
            messagebox.showerror("Error", "Please enter a password!")
            return
            
        if '@' not in email or '.' not in email.split('@')[1]:
            self.log_message(f"❌ Invalid email format: {email}", "ERROR")
            messagebox.showerror("Error", "Please enter a valid email address!")
            return
            
        self.log_message(f"✅ Validation passed for: {email}", "SUCCESS")
        self.log_message("🚀 Starting single account OAuth client generation...", "STEP")
        
        # Disable single generate button
        self.single_generate_btn.config(state="disabled")
        
        # Start generation in separate thread
        thread = threading.Thread(target=self.generate_single_oauth_client)
        thread.daemon = True
        thread.start()
        
    def read_accounts_file(self):
        """Read account information from file"""
        accounts = []
        self.log_message(f"📖 Reading accounts from file: {os.path.basename(self.selected_file.get())}", "STEP")
        try:
            with open(self.selected_file.get(), 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if line and ':' in line:
                        email, password = line.split(':', 1)
                        accounts.append({
                            'email': email.strip(),
                            'password': password.strip(),
                            'line_num': line_num
                        })
                    elif line:  # Non-empty line without colon
                        self.log_message(f"⚠️ Invalid format on line {line_num}: {line}", "WARNING")
                        self.status_var.set(f"Line {line_num}: Invalid format (email:password required)")
            self.log_message(f"✅ Successfully read {len(accounts)} accounts from file", "SUCCESS")        
        except Exception as e:
            self.log_message(f"❌ Error reading file: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Error reading file: {str(e)}")
            return []
            
        return accounts
        
    def generate_oauth_clients(self):
        """Generate OAuth clients for each account"""
        accounts = self.read_accounts_file()
        
        if not accounts:
            self.log_message("❌ No valid accounts found in the file!", "ERROR")
            self.status_var.set("No valid accounts found!")
            self.generate_btn.config(state="normal")
            return
            
        total_accounts = len(accounts)
        successful = 0
        failed = 0
        
        self.log_message(f"🔄 Starting batch processing of {total_accounts} accounts...", "STEP")
        
        for i, account in enumerate(accounts):
            try:
                self.status_var.set(f"Processing: {account['email']} ({i+1}/{total_accounts})")
                self.log_message(f"🔄 Processing account {i+1}/{total_accounts}: {account['email']}", "STEP")
                
                # Generate OAuth client for this account
                success = self.create_oauth_client(account)
                
                if success:
                    successful += 1
                    self.status_var.set(f"Success: {account['email']}")
                    self.log_message(f"✅ Successfully processed: {account['email']}", "SUCCESS")
                else:
                    failed += 1
                    self.status_var.set(f"Failed: {account['email']}")
                    self.log_message(f"❌ Failed to process: {account['email']}", "ERROR")
                    
                # Update progress
                progress = ((i + 1) / total_accounts) * 100
                self.progress_var.set(progress)
                
                # Small delay between accounts
                time.sleep(1)
                
            except Exception as e:
                failed += 1
                self.status_var.set(f"Error: {account['email']} - {str(e)}")
                self.log_message(f"❌ Error processing {account['email']}: {str(e)}", "ERROR")
                
        # Final status
        self.status_var.set(f"Completed! Success: {successful}, Failed: {failed}")
        self.log_message(f"🎉 Batch processing completed! Success: {successful}, Failed: {failed}", "SUCCESS")
        self.generate_btn.config(state="normal")
        
        if successful > 0:
            messagebox.showinfo("Completed", 
                              f"JSON file generation completed!\n"
                              f"Success: {successful}\n"
                              f"Failed: {failed}\n\n"
                              f"Files saved in '{self.output_dir}' folder.")
                              
    def generate_single_oauth_client(self):
        """Generate OAuth client for single account"""
        try:
            # Create account object
            account = {
                'email': self.single_email.get().strip(),
                'password': self.single_password.get().strip(),
                'line_num': 1
            }
            
            self.status_var.set(f"Processing single account: {account['email']}")
            self.progress_var.set(0)
            
            # Generate OAuth client for this account
            success = self.create_oauth_client(account)
            
            if success:
                self.status_var.set(f"Success: Single JSON generated for {account['email']}")
                self.progress_var.set(100)
                messagebox.showinfo("Success", 
                                  f"JSON file generated successfully!\n"
                                  f"Email: {account['email']}\n\n"
                                  f"File saved in '{self.output_dir}' folder.")
                # Clear input fields after successful generation
                self.single_email.set("")
                self.single_password.set("")
            else:
                self.status_var.set(f"Failed: Single JSON generation failed for {account['email']}")
                messagebox.showerror("Error", 
                                   f"Failed to generate JSON file for {account['email']}\n"
                                   f"Please check the credentials and try again.")
                
        except Exception as e:
            self.status_var.set(f"Error: Single account generation - {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            # Re-enable single generate button
            self.single_generate_btn.config(state="normal")
            
    def create_oauth_client(self, account):
        """Create OAuth client for a single account"""
        try:
            self.log_message(f"🔄 Starting OAuth client creation for: {account['email']}", "STEP")
            result = self.setup_selenium_automation(account)
            if result:
                self.log_message(f"✅ OAuth client created successfully for: {account['email']}", "SUCCESS")
            else:
                self.log_message(f"❌ OAuth client creation failed for: {account['email']}", "ERROR")
            return result
            
        except Exception as e:
            error_msg = f"Error creating OAuth client for {account['email']}: {str(e)}"
            print(error_msg)
            self.log_message(f"❌ {error_msg}", "ERROR")
            return False
            
    def setup_selenium_automation(self, account):
        """Selenium automation for Google Cloud Console"""
        driver = None
        try:
            # Chrome options setup with anti-detection measures
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-images')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            # chrome_options.add_argument('--headless')  # Uncomment for headless mode
            
            # Initialize WebDriver
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            
            self.log_message("🚀 Initializing Chrome WebDriver...", "STEP")
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute script to hide WebDriver detection
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            driver.implicitly_wait(10)
            self.log_message("✅ Chrome WebDriver initialized successfully", "SUCCESS")
            
            # Step 1: Login to Google Cloud Console
            self.log_message("🔑 Starting Step 1: Login to Google Cloud Console", "STEP")
            self.status_var.set(f"Logging into Google Cloud Console: {account['email']}")
            login_result = self.login_to_google_cloud(driver, account)
            self.log_message(f"🔍 Login result: {login_result}", "DEBUG")
            if not login_result:
                self.log_message("❌ Step 1 failed: Login to Google Cloud Console", "ERROR")
                return False
            self.log_message("✅ Step 1 completed: Login to Google Cloud Console", "SUCCESS")
                
            # Step 2: Create or select project
            self.log_message("🏗️ Starting Step 2: Create or select project", "STEP")
            self.status_var.set(f"Creating/selecting project: {account['email']}")
            project_id = self.create_or_select_project(driver, account)
            self.log_message(f"🔍 Project ID result: {project_id}", "DEBUG")
            if not project_id:
                self.log_message("❌ Step 2 failed: Create or select project", "ERROR")
                return False
            self.log_message(f"✅ Step 2 completed: Project created/selected with ID: {project_id}", "SUCCESS")
                
            # Step 3: Enable Gmail API
            self.log_message("🔌 Starting Step 3: Enable Gmail API", "STEP")
            self.status_var.set(f"Enabling Gmail API: {account['email']}")
            api_result = self.enable_gmail_api(driver)
            self.log_message(f"🔍 Gmail API enable result: {api_result}", "DEBUG")
            if not api_result:
                self.log_message("❌ Step 3 failed: Enable Gmail API", "ERROR")
                return False
            self.log_message("✅ Step 3 completed: Gmail API enabled", "SUCCESS")
                
            # Step 4: Create OAuth credentials
            self.log_message("🔑 Starting Step 4: Create OAuth credentials", "STEP")
            self.status_var.set(f"Creating OAuth credentials: {account['email']}")
            credentials_data = self.create_oauth_credentials(driver, account)
            self.log_message(f"🔍 OAuth credentials result: {credentials_data}", "DEBUG")
            if not credentials_data:
                self.log_message("❌ Step 4 failed: Create OAuth credentials", "ERROR")
                return False
            self.log_message("✅ Step 4 completed: OAuth credentials created", "SUCCESS")
                
            # Step 5: Save JSON file
            self.log_message("💾 Starting Step 5: Save JSON file", "STEP")
            self.status_var.set(f"Saving JSON file: {account['email']}")
            save_result = self.save_oauth_json(account, credentials_data, project_id)
            self.log_message(f"🔍 JSON save result: {save_result}", "DEBUG")
            if not save_result:
                self.log_message("❌ Step 5 failed: Save JSON file", "ERROR")
                return False
            self.log_message("✅ Step 5 completed: JSON file saved", "SUCCESS")
            
            self.log_message("🎉 All steps completed successfully!", "SUCCESS")
            return True
            
        except Exception as e:
            error_msg = f"Selenium automation error for {account['email']}: {str(e)}"
            self.status_var.set(f"Error: {account['email']} - {str(e)}")
            print(error_msg)
            self.log_message(f"❌ {error_msg}", "ERROR")
            # Print full traceback for debugging
            import traceback
            traceback.print_exc()
            return False
        finally:
            if driver:
                driver.quit()
                
    def login_to_google_cloud(self, driver, account):
        """Login to Google Cloud Console"""
        print(f"🚀 LOGIN METHOD CALLED with email: {account['email']}")
        print(f"🔐 Password length: {len(account['password'])}")
        try:
            # Navigate to Google Cloud Console
            self.log_message("🌐 Navigating to Google Cloud Console...", "STEP")
            print("🌐 Navigating to Google Cloud Console...")
            driver.get("https://console.cloud.google.com/")
            
            # Wait for login page or dashboard with longer timeout
            print("⏳ Waiting for page to load...")
            WebDriverWait(driver, 30).until(
                lambda d: "accounts.google.com" in d.current_url or "console.cloud.google.com" in d.current_url
            )
            
            print(f"📍 Current URL: {driver.current_url}")
            self.log_message(f"📍 Current URL: {driver.current_url}", "INFO")
            
            # If redirected to login page
            if "accounts.google.com" in driver.current_url:
                print("🔐 Login page detected, entering credentials...")
                self.log_message("🔐 Login page detected, entering credentials...", "STEP")
                # Enter email
                print(f"📧 Entering email: {account['email']}")
                self.log_message(f"📧 Entering email: {account['email']}", "STEP")
                try:
                    email_input = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.ID, "identifierId"))
                    )
                    email_input.clear()
                    email_input.send_keys(account['email'])
                    
                    # Click Next
                    next_button = driver.find_element(By.ID, "identifierNext")
                    next_button.click()
                    print("✅ Email entered successfully")
                    self.log_message("✅ Email entered successfully", "SUCCESS")
                except Exception as e:
                    print(f"❌ Failed to enter email: {str(e)}")
                    self.log_message(f"❌ Failed to enter email: {str(e)}", "ERROR")
                    return False
                
                # Wait for password field with longer timeout
                print("🔐 Waiting for password field...")
                self.log_message("🔐 Waiting for password field...", "STEP")
                try:
                    # Try multiple selectors for password field (including div elements)
                    password_input = None
                    selectors = [
                        (By.CSS_SELECTOR, "#password input"),  # Google's actual structure: div#password > input
                        (By.XPATH, "//div[@id='password']//input"),  # Alternative xpath for div structure
                        (By.CSS_SELECTOR, "div[data-initial-value] input"),  # Google's password div structure
                        (By.NAME, "password"),
                        (By.ID, "password"),
                        (By.CSS_SELECTOR, "input[type='password']"),
                        (By.CSS_SELECTOR, "input[name='Passwd']"),
                        (By.XPATH, "//input[@type='password']"),
                        (By.XPATH, "//input[@name='password']"),
                        (By.XPATH, "//input[@name='Passwd']")
                    ]
                    
                    for selector_type, selector_value in selectors:
                        try:
                            self.log_message(f"🔍 Trying password selector: {selector_type} = {selector_value}", "DEBUG")
                            password_input = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((selector_type, selector_value))
                            )
                            self.log_message(f"✅ Password field found with selector: {selector_type} = {selector_value}", "SUCCESS")
                            break
                        except Exception as sel_e:
                            self.log_message(f"❌ Selector failed: {selector_type} = {selector_value}, Error: {sel_e}", "WARNING")
                            continue
                    
                    if password_input is None:
                        # Wait longer and try again
                        print("⏳ Password field not found, waiting longer...")
                        self.log_message("⏳ Password field not found, waiting longer...", "WARNING")
                        time.sleep(3)
                        try:
                            password_input = WebDriverWait(driver, 15).until(
                                EC.element_to_be_clickable((By.NAME, "password"))
                            )
                        except Exception as session_error:
                            print(f"❌ Session error during password field wait: {session_error}")
                            self.log_message(f"❌ Session error during password field wait: {session_error}", "ERROR")
                            return False
                    
                    self.log_message("🔐 Entering password...", "STEP")
                    self.log_message(f"🔍 Password field element: {password_input}", "DEBUG")
                    self.log_message(f"🔍 Password field tag: {password_input.tag_name}", "DEBUG")
                    self.log_message(f"🔍 Password field enabled: {password_input.is_enabled()}", "DEBUG")
                    self.log_message(f"🔍 Password field displayed: {password_input.is_displayed()}", "DEBUG")
                    
                    # Add try-catch around the entire password entry process
                    try:
                        self.log_message("🚀 Starting password entry process...", "DEBUG")
                        # Wait for element to be fully interactive
                        self.log_message("⏳ Waiting 2 seconds for element to be interactive...", "DEBUG")
                        time.sleep(2)
                        self.log_message("✅ Wait completed, proceeding with password entry", "DEBUG")
                        
                        # Try to click first to focus
                        self.log_message("🖱️ Attempting to click password field for focus...", "DEBUG")
                        try:
                            password_input.click()
                            self.log_message("✅ Password field clicked for focus", "SUCCESS")
                            time.sleep(1)
                        except Exception as e:
                            self.log_message(f"⚠️ Failed to click password field: {e}", "WARNING")
                        
                        # Clear and enter password
                        try:
                            password_input.clear()
                            self.log_message("✅ Password field cleared", "SUCCESS")
                        except Exception as e:
                            self.log_message(f"⚠️ Failed to clear password field: {e}", "WARNING")
                        
                        # Enhanced password filling with multiple methods (based on successful test results)
                        password_filled = False
                        
                        # Method 1: Standard Selenium approach
                        try:
                            self.log_message("🔧 Method 1: Standard Selenium input...", "DEBUG")
                            password_input.send_keys(account['password'])
                            
                            # Verify
                            password_value = password_input.get_attribute("value")
                            if len(password_value) == len(account['password']):
                                self.log_message(f"✅ Method 1 successful - Password length: {len(password_value)}", "SUCCESS")
                                password_filled = True
                            else:
                                self.log_message(f"⚠️ Method 1 partial - Expected: {len(account['password'])}, Got: {len(password_value)}", "WARNING")
                                
                        except Exception as e:
                            self.log_message(f"❌ Method 1 failed: {e}", "WARNING")
                         
                        # Method 2: JavaScript approach (proven to work from tests)
                        if not password_filled:
                            try:
                                self.log_message("🔧 Method 2: JavaScript input...", "DEBUG")
                                
                                # Focus the element first
                                driver.execute_script("arguments[0].focus();", password_input)
                                time.sleep(0.5)
                                
                                # Clear and set value
                                driver.execute_script("arguments[0].value = '';", password_input)
                                time.sleep(0.5)
                                driver.execute_script("arguments[0].value = arguments[1];", password_input, account['password'])
                                
                                # Trigger events
                                driver.execute_script("""
                                    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                                    arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                                """, password_input)
                                
                                time.sleep(1)
                                
                                # Verify
                                password_value = password_input.get_attribute("value")
                                if len(password_value) == len(account['password']):
                                    self.log_message(f"✅ Method 2 successful - Password length: {len(password_value)}", "SUCCESS")
                                    password_filled = True
                                else:
                                    self.log_message(f"⚠️ Method 2 partial - Expected: {len(account['password'])}, Got: {len(password_value)}", "WARNING")
                                    
                            except Exception as e:
                                self.log_message(f"❌ Method 2 failed: {e}", "WARNING")
                         
                        # Method 3: Character-by-character input as final fallback
                        if not password_filled:
                            try:
                                self.log_message("🔧 Method 3: Character-by-character input...", "DEBUG")
                                
                                # Clear field first
                                password_input.clear()
                                time.sleep(0.5)
                                
                                # Send each character individually
                                for char in account['password']:
                                    password_input.send_keys(char)
                                    time.sleep(0.1)
                                
                                time.sleep(1)
                                
                                # Verify
                                password_value = password_input.get_attribute("value")
                                if len(password_value) == len(account['password']):
                                    self.log_message(f"✅ Method 3 successful - Password length: {len(password_value)}", "SUCCESS")
                                    password_filled = True
                                else:
                                    self.log_message(f"⚠️ Method 3 partial - Expected: {len(account['password'])}, Got: {len(password_value)}", "WARNING")
                                    
                            except Exception as e:
                                self.log_message(f"❌ Method 3 failed: {e}", "WARNING")
                        
                        if not password_filled:
                            self.log_message("❌ All password filling methods failed", "ERROR")
                            raise Exception("All password filling methods failed")
                            
                        self.log_message(f"🔍 Final password field value length: {len(password_input.get_attribute('value'))}", "DEBUG")
                    
                        # Try multiple selectors for password next button
                        self.log_message("🔍 Looking for Next button...", "STEP")
                        next_button = None
                        next_selectors = [
                            (By.ID, "passwordNext"),
                            (By.CSS_SELECTOR, "#passwordNext"),
                            (By.XPATH, "//button[@id='passwordNext']"),
                            (By.XPATH, "//span[contains(text(), 'Next')]/parent::button"),
                            (By.CSS_SELECTOR, "button[type='submit']"),
                            (By.XPATH, "//div[@id='passwordNext']")
                        ]
                        
                        for selector_type, selector_value in next_selectors:
                            try:
                                next_button = driver.find_element(selector_type, selector_value)
                                self.log_message(f"✅ Next button found with selector: {selector_type} = {selector_value}", "SUCCESS")
                                break
                            except Exception as e:
                                self.log_message(f"❌ Next button selector failed: {selector_type} = {selector_value}", "WARNING")
                                continue
                        
                        if next_button:
                            try:
                                next_button.click()
                                self.log_message("✅ Next button clicked successfully", "SUCCESS")
                            except Exception as e:
                                self.log_message(f"❌ Failed to click Next button: {e}", "ERROR")
                                raise e
                        else:
                            self.log_message("❌ Password Next button not found with any selector", "ERROR")
                            raise Exception("Password Next button not found")
                            
                    except Exception as password_error:
                        self.log_message(f"❌ Password entry process failed: {str(password_error)}", "ERROR")
                        import traceback
                        self.log_message(f"📋 Full traceback: {traceback.format_exc()}", "ERROR")
                        self.log_message(f"📍 Current URL: {driver.current_url}", "INFO")
                        return False
                        
                except Exception as e:
                    self.log_message(f"❌ Failed to enter password: {str(e)}", "ERROR")
                    self.log_message(f"📍 Current URL: {driver.current_url}", "INFO")
                    
                    # Check for error messages on email step
                    try:
                        error_elements = driver.find_elements(By.CSS_SELECTOR, "[role='alert'], .LXRPh, .dEOOab, .Ekjuhf")
                        for error in error_elements:
                            if error.text.strip():
                                self.log_message(f"❌ Error message: {error.text}", "ERROR")
                    except:
                        pass
                    return False
                
                # Wait for result with much longer timeout
                self.log_message("⏳ Waiting for login result...", "STEP")
                time.sleep(5)  # Give more time for page to process
                
                # Check current URL after login attempt
                current_url = driver.current_url
                self.log_message(f"📍 After login URL: {current_url}", "INFO")
                
                # Check for different scenarios
                if "challenge/pwd" in current_url:
                    self.log_message("❌ Password challenge detected - incorrect password", "ERROR")
                    return False
                elif "console.cloud.google.com" in current_url:
                    self.log_message("✅ Login successful - reached Google Cloud Console", "SUCCESS")
                    return True
                elif "challenge" in current_url or "signin/v2/challenge" in current_url:
                    self.log_message("🔐 2FA verification required. Please complete manually...", "WARNING")
                    self.status_var.set(f"2FA required: {account['email']} - Complete manual verification")
                    
                    # Show message to user
                    import tkinter.messagebox as msgbox
                    msgbox.showwarning("2FA Required", 
                                     f"Two-factor authentication is required for {account['email']}\n\n"
                                     "Please complete the verification in the browser window and then click OK.")
                    
                    # Wait for user to complete 2FA manually
                    try:
                        WebDriverWait(driver, 300).until(  # 5 minutes timeout
                            lambda d: "console.cloud.google.com" in d.current_url
                        )
                        self.log_message("✅ 2FA verification completed", "SUCCESS")
                        return True
                    except TimeoutException:
                        self.log_message("❌ 2FA verification timeout", "ERROR")
                        return False
                        
                elif "signin" in current_url:
                    self.log_message("❌ Login failed - still on signin page", "ERROR")
                    
                    # Check for error messages
                    try:
                        error_elements = driver.find_elements(By.CSS_SELECTOR, "[role='alert'], .LXRPh, .dEOOab")
                        for error in error_elements:
                            if error.text.strip():
                                self.log_message(f"❌ Error message: {error.text}", "ERROR")
                    except:
                        pass
                        
                    return False
                elif "myaccount.google.com" in current_url or "accounts.google.com" in current_url:
                    self.log_message("⚠️ Redirected to Google account page - trying to navigate to Cloud Console", "WARNING")
                    try:
                        driver.get("https://console.cloud.google.com/")
                        time.sleep(3)
                        if "console.cloud.google.com" in driver.current_url:
                            self.log_message("✅ Successfully navigated to Google Cloud Console", "SUCCESS")
                            return True
                        else:
                            self.log_message(f"❌ Failed to reach Cloud Console, current URL: {driver.current_url}", "ERROR")
                            return False
                    except Exception as nav_e:
                        self.log_message(f"❌ Navigation error: {nav_e}", "ERROR")
                        return False
                else:
                    self.log_message(f"⚠️ Unexpected URL after login: {current_url}", "WARNING")
                    # Try to navigate to Cloud Console
                    try:
                        driver.get("https://console.cloud.google.com/")
                        time.sleep(3)
                        if "console.cloud.google.com" in driver.current_url:
                            self.log_message("✅ Successfully navigated to Google Cloud Console", "SUCCESS")
                            return True
                        else:
                            self.log_message(f"❌ Failed to reach Cloud Console after redirect, current URL: {driver.current_url}", "ERROR")
                            return False
                    except Exception as nav_e:
                        self.log_message(f"❌ Navigation error after unexpected URL: {nav_e}", "ERROR")
                        return False
            else:
                self.log_message("✅ Already logged in - reached Google Cloud Console directly", "SUCCESS")
                return True
            
        except TimeoutException as e:
            self.log_message(f"⏰ Login timeout: {str(e)}", "ERROR")
            self.log_message(f"📍 Current URL: {driver.current_url}", "INFO")
            self.status_var.set(f"Login timeout: {account['email']}")
            return False
        except Exception as e:
            self.log_message(f"❌ Login error: {str(e)}", "ERROR")
            self.log_message(f"📍 Current URL: {driver.current_url}", "INFO")
            self.status_var.set(f"Login error: {account['email']} - {str(e)}")
            return False
            
    def create_or_select_project(self, driver, account):
        """Create or select project"""
        try:
            self.log_message("🏗️ Creating new Google Cloud project...", "STEP")
            # Generate project ID
            project_id = f"gmail-oauth-{account['email'].split('@')[0]}-{int(time.time())}"
            
            # Click on project selector
            try:
                project_selector = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='project-switcher-button']"))
                )
                project_selector.click()
            except:
                # Alternative selector
                project_selector = driver.find_element(By.CSS_SELECTOR, ".cfc-project-switcher-button")
                project_selector.click()
            
            # Click "New Project"
            new_project_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'New Project')]"))
            )
            new_project_btn.click()
            
            # Enter project name
            project_name = f"Gmail OAuth {account['email'].split('@')[0]}"
            self.log_message(f"📝 Creating project with name: {project_name}", "STEP")
            project_name_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "p6ntest-project-name-input"))
            )
            project_name_input.clear()
            project_name_input.send_keys(project_name)
            
            # Project ID will be auto-generated, but we can modify if needed
            time.sleep(2)
            
            # Click Create
            create_btn = driver.find_element(By.XPATH, "//span[contains(text(), 'Create')]/parent::button")
            create_btn.click()
            
            self.log_message("⏳ Waiting for project creation to complete...", "STEP")
            # Wait for project creation
            WebDriverWait(driver, 30).until(
                lambda d: "Project created" in d.page_source or "dashboard" in d.current_url.lower()
            )
            
            self.log_message(f"✅ Project created successfully: {project_name}", "SUCCESS")
            return project_id
            
        except Exception as e:
            self.log_message(f"❌ Error creating project: {e}", "ERROR")
            self.status_var.set(f"Project creation error: {str(e)}")
            return None
            
    def enable_gmail_api(self, driver):
        """Enable Gmail API"""
        try:
            self.log_message("🔌 Enabling Gmail API...", "STEP")
            # Navigate to APIs & Services > Library
            driver.get("https://console.cloud.google.com/apis/library")
            
            self.log_message("🔍 Searching for Gmail API...", "STEP")
            # Search for Gmail API
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Search']"))
            )
            search_box.clear()
            search_box.send_keys("Gmail API")
            search_box.submit()
            
            # Click on Gmail API
            gmail_api_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'gmail')]//div[contains(text(), 'Gmail API')]"))
            )
            gmail_api_link.click()
            
            self.log_message("⚡ Enabling Gmail API for the project...", "STEP")
            # Click Enable
            try:
                enable_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Enable')]/parent::button"))
                )
                enable_btn.click()
                
                # Wait for API to be enabled
                WebDriverWait(driver, 20).until(
                    lambda d: "API enabled" in d.page_source or "Manage" in d.page_source
                )
            except:
                # API might already be enabled
                if "Manage" in driver.page_source:
                    pass  # Already enabled
                else:
                    raise
            
            self.log_message("✅ Gmail API enabled successfully", "SUCCESS")
            return True
            
        except Exception as e:
            self.log_message(f"❌ Error enabling Gmail API: {e}", "ERROR")
            self.status_var.set(f"Gmail API enable error: {str(e)}")
            return False
            
    def create_oauth_credentials(self, driver, account):
        """Create OAuth credentials"""
        try:
            self.log_message("🔑 Creating OAuth 2.0 Client ID...", "STEP")
            # Navigate to Credentials page
            driver.get("https://console.cloud.google.com/apis/credentials")
            
            # Click "Create Credentials"
            create_credentials_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Create Credentials')]/parent::button"))
            )
            create_credentials_btn.click()
            
            # Select "OAuth client ID"
            oauth_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'OAuth client ID')]"))
            )
            oauth_option.click()
            
            # Configure OAuth consent screen if needed
            try:
                configure_btn = driver.find_element(By.XPATH, "//span[contains(text(), 'Configure Consent Screen')]/parent::button")
                configure_btn.click()
                
                self.log_message("🔐 Setting up OAuth consent screen...", "STEP")
                
                # Select External
                external_radio = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@value='EXTERNAL']"))
                )
                external_radio.click()
                
                # Click Create
                create_btn = driver.find_element(By.XPATH, "//span[contains(text(), 'Create')]/parent::button")
                create_btn.click()
                
                self.log_message("📋 Filling OAuth consent screen details...", "STEP")
                # Fill OAuth consent screen
                app_name_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label*='App name']"))
                )
                app_name_input.send_keys(f"Gmail OAuth App {account['email'].split('@')[0]}")
                
                # User support email
                support_email = driver.find_element(By.CSS_SELECTOR, "input[aria-label*='User support email']")
                support_email.send_keys(account['email'])
                
                # Developer contact email
                dev_email = driver.find_element(By.CSS_SELECTOR, "input[aria-label*='Developer contact information']")
                dev_email.send_keys(account['email'])
                
                # Save and Continue
                save_btn = driver.find_element(By.XPATH, "//span[contains(text(), 'Save and Continue')]/parent::button")
                save_btn.click()
                
                self.log_message("⏭️ Skipping scopes and test users configuration...", "STEP")
                # Skip scopes for now
                save_continue_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Save and Continue')]/parent::button"))
                )
                save_continue_btn.click()
                
                # Skip test users
                save_continue_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Save and Continue')]/parent::button"))
                )
                save_continue_btn.click()
                
                # Back to dashboard
                back_dashboard_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Back to Dashboard')]/parent::button"))
                )
                back_dashboard_btn.click()
                
                self.log_message("✅ OAuth consent screen configured successfully", "SUCCESS")
                
                # Go back to credentials
                driver.get("https://console.cloud.google.com/apis/credentials")
                
                # Try creating credentials again
                create_credentials_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Create Credentials')]/parent::button"))
                )
                create_credentials_btn.click()
                
                oauth_option = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'OAuth client ID')]"))
                )
                oauth_option.click()
                
            except:
                pass  # Consent screen might already be configured
            
            self.log_message("🖥️ Configuring OAuth client for desktop application...", "STEP")
            # Select application type (Desktop application)
            app_type_dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label*='Application type']"))
            )
            app_type_dropdown.click()
            
            desktop_option = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Desktop application')]"))
            )
            desktop_option.click()
            
            # Enter name
            name_input = driver.find_element(By.CSS_SELECTOR, "input[aria-label*='Name']")
            name_input.send_keys(f"Gmail OAuth Client {account['email'].split('@')[0]}")
            
            # Click Create
            create_btn = driver.find_element(By.XPATH, "//span[contains(text(), 'Create')]/parent::button")
            create_btn.click()
            
            self.log_message("⏳ Waiting for OAuth client creation...", "STEP")
            # Wait for credentials to be created and get the data
            WebDriverWait(driver, 15).until(
                lambda d: "Client ID" in d.page_source and "Client secret" in d.page_source
            )
            
            # Extract client ID and secret
            client_id_element = driver.find_element(By.XPATH, "//span[contains(text(), 'Client ID')]/following-sibling::span")
            client_secret_element = driver.find_element(By.XPATH, "//span[contains(text(), 'Client secret')]/following-sibling::span")
            
            credentials_data = {
                'client_id': client_id_element.text,
                'client_secret': client_secret_element.text
            }
            
            # Close the dialog
            close_btn = driver.find_element(By.XPATH, "//span[contains(text(), 'OK')]/parent::button")
            close_btn.click()
            
            self.log_message("✅ OAuth credentials created successfully", "SUCCESS")
            return credentials_data
            
        except Exception as e:
            self.log_message(f"❌ OAuth credentials creation error: {e}", "ERROR")
            self.status_var.set(f"OAuth credentials creation error: {str(e)}")
            return None
            
    def save_oauth_json(self, account, credentials_data, project_id):
        """Save OAuth JSON file"""
        try:
            self.log_message("💾 Preparing OAuth JSON data...", "STEP")
            oauth_data = {
                "installed": {
                    "client_id": credentials_data['client_id'],
                    "client_secret": credentials_data['client_secret'],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "redirect_uris": ["http://localhost"]
                },
                "account_info": {
                    "email": account['email'],
                    "project_id": project_id,
                    "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            
            # Save JSON file
            filename = f"{account['email'].replace('@', '_').replace('.', '_')}.json"
            filepath = os.path.join(self.output_dir, filename)
            
            self.log_message(f"📁 Saving OAuth JSON as: {filename}", "STEP")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(oauth_data, f, indent=2, ensure_ascii=False)
                
            self.log_message(f"✅ OAuth JSON saved successfully: {filename}", "SUCCESS")
            return True
            
        except Exception as e:
            self.log_message(f"❌ JSON save error: {e}", "ERROR")
            self.status_var.set(f"JSON save error: {str(e)}")
            return False

def main():
    """Main function"""
    root = tk.Tk()
    app = GmailOAuthGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()