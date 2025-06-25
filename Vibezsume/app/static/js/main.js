// Ultra-Modern JavaScript for Vibezsume Resume Analysis Platform ✨

class VibezsumApp {
    constructor() {
        this.currentTheme = 'light';
        this.animations = new Map();
        this.skills = []; // Initialize skills array
        this.experienceCount = 0;
        this.educationCount = 0;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeComponents();
        this.setupScrollAnimations();
        this.setupNavbarEffects();
        this.showWelcomeAnimation();
    }

    // ✨ Modern Animation System
    setupScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    this.triggerElementAnimation(entry.target);
                }
            });
        }, observerOptions);

        // Observe all elements with animate-on-scroll class
        document.querySelectorAll('.animate-on-scroll').forEach(el => {
            observer.observe(el);
        });
    }

    triggerElementAnimation(element) {
        const animationType = element.dataset.animation || 'fadeInUp';
        element.style.animationDelay = `${Math.random() * 0.5}s`;
        element.style.animation = `${animationType} 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards`;
    }

    // 🎯 Enhanced Navbar Effects
    setupNavbarEffects() {
        const navbar = document.getElementById('navbar');
        let lastScroll = 0;

        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;
            
            // Add/remove scrolled class for styling
            if (currentScroll > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }

            // Hide/show navbar on scroll
            if (currentScroll > lastScroll && currentScroll > 200) {
                navbar.style.transform = 'translateY(-100%)';
            } else {
                navbar.style.transform = 'translateY(0)';
            }
            
            lastScroll = currentScroll;
        });
    }

    // 🎉 Welcome Animation
    showWelcomeAnimation() {
        // Create floating particles
        this.createFloatingParticles();
        
        // Animate hero elements
        setTimeout(() => {
            document.querySelector('.hero-content').style.animation = 'slideInLeft 1s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards';
            document.querySelector('.hero-image').style.animation = 'slideInRight 1s cubic-bezier(0.68, -0.55, 0.265, 1.55) 0.3s forwards';
        }, 100);
    }

    createFloatingParticles() {
        const hero = document.querySelector('.hero');
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.className = 'floating-particle';
            particle.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation: float ${3 + Math.random() * 4}s ease-in-out infinite;
                animation-delay: ${Math.random() * 2}s;
                pointer-events: none;
            `;
            hero.appendChild(particle);
        }
    }

    setupEventListeners() {
        // Enhanced Navigation with smooth scrolling
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = e.target.getAttribute('href').substring(1);
                this.smoothScrollToSection(target);
                this.addRippleEffect(e.target, e);
            });
        });

        // Resume Analyzer with enhanced UX
        this.setupResumeAnalyzer();
        
        // Resume Builder with live preview
        this.setupResumeBuilder();
        
        // ATS Validator with real-time feedback
        this.setupATSValidator();

        // Global keyboard shortcuts
        this.setupKeyboardShortcuts();
    }

    // 🎨 Ripple Effect for buttons
    addRippleEffect(element, event) {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s ease-out forwards;
            pointer-events: none;
        `;
        
        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    }

    // 🚀 Enhanced Smooth Scrolling
    smoothScrollToSection(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            const headerHeight = document.querySelector('.navbar').offsetHeight;
            const targetPosition = section.offsetTop - headerHeight - 20;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });

            // Add visual feedback
            section.style.animation = 'highlight 1s ease-out';
            setTimeout(() => {
                section.style.animation = '';
            }, 1000);
        }
    }

    // ⌨️ Keyboard Shortcuts
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch(e.key) {
                    case '1':
                        e.preventDefault();
                        this.smoothScrollToSection('home');
                        break;
                    case '2':
                        e.preventDefault();
                        this.smoothScrollToSection('analyzer');
                        break;
                    case '3':
                        e.preventDefault();
                        this.smoothScrollToSection('builder');
                        break;
                    case '4':
                        e.preventDefault();
                        this.smoothScrollToSection('validator');
                        break;
                }
            }
        });
    }    setupResumeAnalyzer() {
        const uploadBox = document.getElementById('uploadBox');
        const fileInput = document.getElementById('resumeFile');
        const analyzeBtn = document.getElementById('analyzeBtn');

        // Enhanced file upload with visual feedback
        uploadBox.addEventListener('click', () => {
            fileInput.click();
            this.addRippleEffect(uploadBox, { clientX: uploadBox.offsetWidth/2, clientY: uploadBox.offsetHeight/2 });
        });

        uploadBox.addEventListener('dragover', this.handleDragOver.bind(this));
        uploadBox.addEventListener('drop', this.handleDrop.bind(this));
        uploadBox.addEventListener('dragleave', this.handleDragLeave.bind(this));

        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleFileSelect(e.target.files[0]);
            }
        });

        analyzeBtn.addEventListener('click', (e) => {
            this.addRippleEffect(e.target, e);
            this.analyzeResume();
        });

        // Enhanced tab switching with animations
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.addRippleEffect(e.target, e);
                this.switchTab(e.target.dataset.tab);
            });
        });
    }

    // 🎨 Enhanced Drag & Drop with visual feedback
    handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        e.currentTarget.classList.add('dragover');
        e.currentTarget.style.transform = 'scale(1.02)';
    }

    handleDragLeave(e) {
        e.preventDefault();
        e.stopPropagation();
        e.currentTarget.classList.remove('dragover');
        e.currentTarget.style.transform = 'scale(1)';
    }

    handleDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        e.currentTarget.classList.remove('dragover');
        e.currentTarget.style.transform = 'scale(1)';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.handleFileSelect(files[0]);
            this.showToast('File uploaded successfully! 🎉', 'success');
        }
    }

    // ✨ Enhanced file selection with validation
    handleFileSelect(file) {
        const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword'];
        const maxSize = 10 * 1024 * 1024; // 10MB

        if (!allowedTypes.includes(file.type)) {
            this.showToast('Please upload a PDF or Word document 📄', 'error');
            return;
        }

        if (file.size > maxSize) {
            this.showToast('File size must be less than 10MB 📏', 'error');
            return;
        }

        // Update UI with file info
        const uploadContent = document.querySelector('.upload-content');
        uploadContent.innerHTML = `
            <i class="fas fa-file-check" style="color: var(--secondary-color);"></i>
            <h3>✅ File Ready!</h3>
            <p><strong>${file.name}</strong></p>
            <p class="file-types">📊 ${(file.size / 1024 / 1024).toFixed(2)} MB • ${file.type.includes('pdf') ? 'PDF' : 'Word'} Document</p>
        `;

        // Enable analyze button with animation
        const analyzeBtn = document.getElementById('analyzeBtn');
        analyzeBtn.disabled = false;
        analyzeBtn.style.animation = 'glow 2s infinite';
        
        this.currentFile = file;
    }

    // 🚀 Enhanced analysis with loading states
    async analyzeResume() {
        if (!this.currentFile) {
            this.showToast('Please upload a file first! 📎', 'warning');
            return;
        }

        this.showLoadingOverlay('🧠 Analyzing your resume with AI...');

        try {
            const formData = new FormData();
            formData.append('file', this.currentFile);
            
            const jobDescription = document.getElementById('jobDescription').value;
            const jobUrl = document.getElementById('jobUrl').value;
            
            if (jobDescription) formData.append('job_description', jobDescription);
            if (jobUrl) formData.append('job_url', jobUrl);

            const response = await fetch('/api/resume/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            this.displayAnalysisResults(result);
            this.showToast('Analysis complete! 🎯', 'success');

        } catch (error) {
            console.error('Analysis error:', error);
            this.showToast('Analysis failed. Please try again! ❌', 'error');
        } finally {
            this.hideLoadingOverlay();
        }
    }

    // 📊 Enhanced results display with animations
    displayAnalysisResults(results) {
        const resultsContainer = document.getElementById('analysisResults');
        resultsContainer.style.display = 'block';
        resultsContainer.style.animation = 'slideInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards';
        
        // Animate score counter
        this.animateScore(results.score || 75);
        
        // Display detailed results
        this.updateAnalysisDetails(results);
        
        // Scroll to results with smooth animation
        setTimeout(() => {
            resultsContainer.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
        }, 300);
    }

    // 🎯 Animated score counter
    animateScore(targetScore) {
        const scoreElement = document.querySelector('.score-value');
        let currentScore = 0;
        const increment = targetScore / 60; // 60 frames for 1 second animation
        
        const updateScore = () => {
            currentScore += increment;
            if (currentScore >= targetScore) {
                currentScore = targetScore;
                scoreElement.textContent = Math.round(currentScore);
                return;
            }
            scoreElement.textContent = Math.round(currentScore);
            requestAnimationFrame(updateScore);
        };
        
        requestAnimationFrame(updateScore);
    }

    // 🎨 Enhanced tab switching with smooth transitions
    switchTab(tabName) {
        // Remove active class from all tabs and panes
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-pane').forEach(pane => {
            pane.classList.remove('active');
            pane.style.opacity = '0';
            pane.style.transform = 'translateY(20px)';
        });

        // Add active class to selected tab
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        
        // Show selected pane with animation
        setTimeout(() => {
            const targetPane = document.getElementById(tabName);
            targetPane.classList.add('active');
            targetPane.style.opacity = '1';
            targetPane.style.transform = 'translateY(0)';
            targetPane.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        }, 100);
    }

    setupResumeBuilder() {
        const form = document.getElementById('resumeBuilderForm');
        const addExperienceBtn = document.getElementById('addExperience');
        const addEducationBtn = document.getElementById('addEducation');
        const addSkillBtn = document.getElementById('addSkill');
        const skillInput = document.getElementById('skillInput');

        // Dynamic form sections
        addExperienceBtn.addEventListener('click', () => this.addExperienceItem());
        addEducationBtn.addEventListener('click', () => this.addEducationItem());
        addSkillBtn.addEventListener('click', () => this.addSkill());
        
        skillInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.addSkill();
            }
        });

        form.addEventListener('submit', this.buildResume.bind(this));

        // Initialize with one experience and education item
        this.addExperienceItem();
        this.addEducationItem();
    }

    setupATSValidator() {
        const methodTabs = document.querySelectorAll('.method-tab');
        const validatorUploadBox = document.getElementById('validatorUploadBox');
        const validatorFile = document.getElementById('validatorFile');
        const validateBtn = document.getElementById('validateBtn');

        // Method switching
        methodTabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.switchValidatorMethod(e.target.dataset.method);
            });
        });

        // File upload for validator
        validatorUploadBox.addEventListener('click', () => validatorFile.click());
        validatorUploadBox.addEventListener('dragover', this.handleDragOver.bind(this));
        validatorUploadBox.addEventListener('drop', this.handleValidatorDrop.bind(this));

        validatorFile.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleValidatorFileSelect(e.target.files[0]);
            }
        });

        validateBtn.addEventListener('click', this.validateResume.bind(this));
    }

    initializeComponents() {
        // Add CSS for new animations
        const style = document.createElement('style');
        style.textContent = `
            @keyframes ripple {
                to { transform: scale(4); opacity: 0; }
            }
            
            @keyframes highlight {
                0%, 100% { background-color: transparent; }
                50% { background-color: rgba(102, 126, 234, 0.1); }
            }
            
            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .analysis-section {
                margin-bottom: 2rem;
                padding: 1.5rem;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 12px;
                border-left: 4px solid var(--primary-color);
            }
            
            .analysis-section h5 {
                color: var(--text-primary);
                margin-bottom: 1rem;
                font-size: 1.1rem;
                font-weight: 700;
            }
            
            .analysis-section ul {
                list-style: none;
                padding: 0;
            }
            
            .analysis-section li {
                display: flex;
                align-items: flex-start;
                gap: 0.8rem;
                margin-bottom: 0.8rem;
                color: var(--text-secondary);
                line-height: 1.5;
            }
            
            .analysis-section li i {
                margin-top: 0.2rem;
                font-size: 0.9rem;
            }
            
            .strength-list li i { color: var(--secondary-color); }
            .suggestion-list li i { color: var(--accent-color); }
            .weakness-list li i { color: #ef4444; }
            
            .floating-particle {
                z-index: 0;
            }
        `;
        document.head.appendChild(style);
        
        // Initialize tooltips, if needed
        this.initializeTooltips();
    }

    initializeTooltips() {
        // Add hover effects for interactive elements
        document.querySelectorAll('[data-tooltip]').forEach(element => {
            element.addEventListener('mouseenter', (e) => {
                const tooltip = document.createElement('div');
                tooltip.className = 'tooltip';
                tooltip.textContent = e.target.dataset.tooltip;
                document.body.appendChild(tooltip);
                
                const rect = e.target.getBoundingClientRect();
                tooltip.style.cssText = `
                    position: absolute;
                    top: ${rect.top - 40}px;
                    left: ${rect.left + rect.width / 2}px;
                    transform: translateX(-50%);
                    background: var(--background-dark);
                    color: white;
                    padding: 0.5rem 1rem;
                    border-radius: 6px;
                    font-size: 0.8rem;
                    z-index: 10000;
                    pointer-events: none;
                    opacity: 0;
                    transition: opacity 0.3s ease;
                `;
                
                setTimeout(() => tooltip.style.opacity = '1', 10);
                
                e.target.addEventListener('mouseleave', () => {
                    tooltip.remove();
                }, { once: true });
            });
        });
    }

    // 🎨 Modern Toast Notification System
    showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icon = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        }[type] || 'ℹ️';
        
        toast.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.2rem;">${icon}</span>
                <span>${message}</span>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        // Trigger animation
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Auto remove
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    }

    // 🔄 Enhanced Loading Overlay
    showLoadingOverlay(message = 'Processing...') {
        const overlay = document.getElementById('loadingOverlay');
        const loadingText = document.getElementById('loadingText');
        
        loadingText.textContent = message;
        overlay.classList.add('active');
        
        // Add pulsing animation to the text
        loadingText.style.animation = 'pulse 2s infinite';
    }

    hideLoadingOverlay() {
        const overlay = document.getElementById('loadingOverlay');
        overlay.classList.remove('active');
    }

    // 📊 Update analysis details with enhanced formatting
    updateAnalysisDetails(results) {
        const detailsContainer = document.getElementById('analysisDetails');
        
        detailsContainer.innerHTML = `
            <div class="analysis-section">
                <h5>💪 Strengths</h5>
                <ul class="strength-list">
                    ${(results.strengths || ['Good overall structure', 'Clear contact information']).map(strength => 
                        `<li><i class="fas fa-check-circle"></i> ${strength}</li>`
                    ).join('')}
                </ul>
            </div>
            
            <div class="analysis-section">
                <h5>🎯 Recommendations</h5>
                <ul class="suggestion-list">
                    ${(results.suggestions || ['Add more quantified achievements', 'Include relevant keywords']).map(suggestion => 
                        `<li><i class="fas fa-lightbulb"></i> ${suggestion}</li>`
                    ).join('')}
                </ul>
            </div>
            
            <div class="analysis-section">
                <h5>🔍 Areas to Improve</h5>
                <ul class="weakness-list">
                    ${(results.weaknesses || ['Could use more specific metrics', 'Consider adding a summary section']).map(weakness => 
                        `<li><i class="fas fa-exclamation-triangle"></i> ${weakness}</li>`
                    ).join('')}
                </ul>
            </div>
        `;
        
        // Add smooth reveal animation for each section
        const sections = detailsContainer.querySelectorAll('.analysis-section');
        sections.forEach((section, index) => {
            section.style.opacity = '0';
            section.style.transform = 'translateY(20px)';
            setTimeout(() => {
                section.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
                section.style.opacity = '1';
                section.style.transform = 'translateY(0)';
            }, index * 200);
        });
    }

    // Utility Functions
    scrollToSection(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            section.scrollIntoView({ behavior: 'smooth' });
        }
    }

    showLoading(text = 'Processing...') {
        const overlay = document.getElementById('loadingOverlay');
        const loadingText = document.getElementById('loadingText');
        loadingText.textContent = text;
        overlay.style.display = 'flex';
    }

    hideLoading() {
        document.getElementById('loadingOverlay').style.display = 'none';
    }

    showToast(message, type = 'success') {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 4000);
    }

    // File Handling
    handleDragOver(e) {
        e.preventDefault();
        e.currentTarget.classList.add('dragover');
    }

    handleDrop(e) {
        e.preventDefault();
        e.currentTarget.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.handleFileSelect(files[0]);
        }
    }

    handleFileSelect(file) {
        if (!this.validateFile(file)) return;
        
        const uploadBox = document.getElementById('uploadBox');
        uploadBox.innerHTML = `
            <div class="upload-content">
                <i class="fas fa-file-check"></i>
                <h3>File Selected</h3>
                <p>${file.name}</p>
                <p class="file-types">Ready to analyze</p>
            </div>
        `;
        
        document.getElementById('analyzeBtn').disabled = false;
        this.selectedFile = file;
    }

    handleValidatorDrop(e) {
        e.preventDefault();
        e.currentTarget.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.handleValidatorFileSelect(files[0]);
        }
    }

    handleValidatorFileSelect(file) {
        if (!this.validateFile(file)) return;
        
        const uploadBox = document.getElementById('validatorUploadBox');
        uploadBox.innerHTML = `
            <div class="upload-content">
                <i class="fas fa-file-check"></i>
                <h3>File Selected for Validation</h3>
                <p>${file.name}</p>
                <p class="file-types">Ready to validate</p>
            </div>
        `;
        
        this.selectedValidatorFile = file;
    }

    validateFile(file) {
        const maxSize = 10 * 1024 * 1024; // 10MB
        const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        
        if (file.size > maxSize) {
            this.showToast('File too large. Maximum size is 10MB.', 'error');
            return false;
        }
        
        if (!allowedTypes.includes(file.type) && !file.name.toLowerCase().endsWith('.doc')) {
            this.showToast('Unsupported file type. Please use PDF or DOCX.', 'error');
            return false;
        }
        
        return true;
    }

    // Resume Analysis
    async analyzeResume() {
        if (!this.selectedFile) {
            this.showToast('Please select a resume file first.', 'error');
            return;
        }

        this.showLoading('Analyzing your resume...');

        try {
            const formData = new FormData();
            formData.append('file', this.selectedFile);
            
            const jobDescription = document.getElementById('jobDescription').value;
            const jobUrl = document.getElementById('jobUrl').value;
            
            if (jobDescription) formData.append('job_description', jobDescription);
            if (jobUrl) formData.append('job_url', jobUrl);

            const response = await fetch('/api/resume/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            this.displayAnalysisResults(result);
            
            this.showToast('Resume analysis completed!', 'success');
        } catch (error) {
            console.error('Analysis error:', error);
            this.showToast('Error analyzing resume. Please try again.', 'error');
        } finally {
            this.hideLoading();
        }
    }

    displayAnalysisResults(result) {
        const resultsDiv = document.getElementById('analysisResults');
        resultsDiv.style.display = 'block';

        // Update score
        const scoreValue = document.querySelector('.score-value');
        scoreValue.textContent = Math.round(result.analysis.score);

        // Update analysis details
        const analysisDetails = document.getElementById('analysisDetails');
        analysisDetails.innerHTML = `
            <div class="analysis-section">
                <h5>Strengths</h5>
                <ul>
                    ${result.analysis.strengths.map(strength => `<li>${strength}</li>`).join('')}
                </ul>
            </div>
            <div class="analysis-section">
                <h5>Areas for Improvement</h5>
                <ul>
                    ${result.analysis.weaknesses.map(weakness => `<li>${weakness}</li>`).join('')}
                </ul>
            </div>
            <div class="analysis-section">
                <h5>Suggestions</h5>
                <ul>
                    ${result.analysis.suggestions.map(suggestion => `<li>${suggestion}</li>`).join('')}
                </ul>
            </div>
        `;

        // Update skills gap if available
        if (result.skill_gap) {
            const skillsContent = document.getElementById('skillsContent');
            skillsContent.innerHTML = `
                <div class="skills-match">
                    <h5>Skill Match: ${result.skill_gap.skill_match_percentage.toFixed(1)}%</h5>
                    <div class="missing-skills">
                        <h6>Missing Required Skills:</h6>
                        <div class="skill-list">
                            ${result.skill_gap.missing_required_skills.map(skill => 
                                `<span class="skill-tag missing">${skill}</span>`
                            ).join('')}
                        </div>
                    </div>
                    <div class="ai-recommendations">
                        <h6>AI Recommendations:</h6>
                        <p>${result.skill_gap.ai_recommendations}</p>
                    </div>
                </div>
            `;
        }

        // Update vibe check
        const vibeContent = document.getElementById('vibeContent');
        vibeContent.innerHTML = `
            <div class="vibe-feedback">
                <p>${result.vibe_feedback}</p>
            </div>
        `;

        // Scroll to results
        resultsDiv.scrollIntoView({ behavior: 'smooth' });
    }

    // Tab Switching
    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-pane').forEach(pane => {
            pane.classList.remove('active');
        });
        document.getElementById(tabName).classList.add('active');
    }

    switchValidatorMethod(method) {
        // Update method tabs
        document.querySelectorAll('.method-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-method="${method}"]`).classList.add('active');

        // Update method content
        document.querySelectorAll('.method-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${method}Method`).classList.add('active');
    }

    // Resume Builder Functions
    addExperienceItem() {
        this.experienceCount++;
        const container = document.getElementById('experienceContainer');
        const experienceDiv = document.createElement('div');
        experienceDiv.className = 'experience-item';
        experienceDiv.innerHTML = `
            <div class="form-row">
                <div class="form-group">
                    <label>Company</label>
                    <input type="text" name="experience_company_${this.experienceCount}" placeholder="Company Name">
                </div>
                <div class="form-group">
                    <label>Position</label>
                    <input type="text" name="experience_position_${this.experienceCount}" placeholder="Job Title">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Start Date</label>
                    <input type="text" name="experience_start_${this.experienceCount}" placeholder="MM/YYYY">
                </div>
                <div class="form-group">
                    <label>End Date</label>
                    <input type="text" name="experience_end_${this.experienceCount}" placeholder="MM/YYYY or Present">
                </div>
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea name="experience_desc_${this.experienceCount}" rows="3" 
                    placeholder="• Describe your responsibilities and achievements&#10;• Use bullet points&#10;• Include metrics and results"></textarea>
            </div>
            <div class="form-group">
                <label>Technologies</label>
                <input type="text" name="experience_tech_${this.experienceCount}" placeholder="Comma-separated list of technologies">
            </div>
            <button type="button" class="btn btn-sm" onclick="this.parentElement.remove()">
                <i class="fas fa-trash"></i> Remove
            </button>
        `;
        container.appendChild(experienceDiv);
    }

    addEducationItem() {
        this.educationCount++;
        const container = document.getElementById('educationContainer');
        const educationDiv = document.createElement('div');
        educationDiv.className = 'education-item';
        educationDiv.innerHTML = `
            <div class="form-row">
                <div class="form-group">
                    <label>Institution</label>
                    <input type="text" name="education_institution_${this.educationCount}" placeholder="University/College Name">
                </div>
                <div class="form-group">
                    <label>Degree</label>
                    <input type="text" name="education_degree_${this.educationCount}" placeholder="Degree Type">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Field of Study</label>
                    <input type="text" name="education_field_${this.educationCount}" placeholder="Major/Field">
                </div>
                <div class="form-group">
                    <label>Graduation Year</label>
                    <input type="text" name="education_year_${this.educationCount}" placeholder="YYYY">
                </div>
            </div>
            <button type="button" class="btn btn-sm" onclick="this.parentElement.remove()">
                <i class="fas fa-trash"></i> Remove
            </button>
        `;
        container.appendChild(educationDiv);
    }

    addSkill() {
        const skillInput = document.getElementById('skillInput');
        const skillName = skillInput.value.trim();
        
        if (!skillName) return;
        
        if (this.skills.includes(skillName)) {
            this.showToast('Skill already added.', 'warning');
            return;
        }
        
        this.skills.push(skillName);
        this.updateSkillsDisplay();
        skillInput.value = '';
    }

    removeSkill(skillName) {
        this.skills = this.skills.filter(skill => skill !== skillName);
        this.updateSkillsDisplay();
    }

    updateSkillsDisplay() {
        const container = document.getElementById('skillsContainer');
        container.innerHTML = this.skills.map(skill => `
            <div class="skill-tag">
                ${skill}
                <button type="button" onclick="app.removeSkill('${skill}')">×</button>
            </div>
        `).join('');
    }

    // Resume Building
    async buildResume(e) {
        e.preventDefault();
        
        this.showLoading('Building your resume...');

        try {
            const formData = new FormData(e.target);
            
            // Add skills to form data
            formData.append('skills_json', JSON.stringify(
                this.skills.map(skill => ({ name: skill, level: 'intermediate' }))
            ));
            
            // Collect experience data
            const experienceData = this.collectExperienceData();
            formData.append('experience_json', JSON.stringify(experienceData));
            
            // Collect education data
            const educationData = this.collectEducationData();
            formData.append('education_json', JSON.stringify(educationData));

            const response = await fetch('/api/builder/build-from-form', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            
            // Open download link
            const downloadUrl = result.download_url;
            window.open(downloadUrl, '_blank');
            
            this.showToast('Resume built successfully!', 'success');
        } catch (error) {
            console.error('Build error:', error);
            this.showToast('Error building resume. Please try again.', 'error');
        } finally {
            this.hideLoading();
        }
    }

    collectExperienceData() {
        const experiences = [];
        const container = document.getElementById('experienceContainer');
        const items = container.querySelectorAll('.experience-item');
        
        items.forEach((item, index) => {
            const company = item.querySelector(`[name="experience_company_${index + 1}"]`)?.value;
            const position = item.querySelector(`[name="experience_position_${index + 1}"]`)?.value;
            const startDate = item.querySelector(`[name="experience_start_${index + 1}"]`)?.value;
            const endDate = item.querySelector(`[name="experience_end_${index + 1}"]`)?.value;
            const description = item.querySelector(`[name="experience_desc_${index + 1}"]`)?.value;
            const technologies = item.querySelector(`[name="experience_tech_${index + 1}"]`)?.value;
            
            if (company && position) {
                experiences.push({
                    company,
                    position,
                    start_date: startDate,
                    end_date: endDate,
                    description: description ? description.split('\n').filter(line => line.trim()) : [],
                    technologies: technologies ? technologies.split(',').map(tech => tech.trim()) : []
                });
            }
        });
        
        return experiences;
    }

    collectEducationData() {
        const educations = [];
        const container = document.getElementById('educationContainer');
        const items = container.querySelectorAll('.education-item');
        
        items.forEach((item, index) => {
            const institution = item.querySelector(`[name="education_institution_${index + 1}"]`)?.value;
            const degree = item.querySelector(`[name="education_degree_${index + 1}"]`)?.value;
            const field = item.querySelector(`[name="education_field_${index + 1}"]`)?.value;
            const year = item.querySelector(`[name="education_year_${index + 1}"]`)?.value;
            
            if (institution && degree) {
                educations.push({
                    institution,
                    degree,
                    field_of_study: field,
                    end_date: year
                });
            }
        });
        
        return educations;
    }

    // ATS Validation
    async validateResume() {
        const activeMethod = document.querySelector('.method-tab.active').dataset.method;
        
        this.showLoading('Validating ATS compatibility...');

        try {
            let response;
            
            if (activeMethod === 'file') {
                if (!this.selectedValidatorFile) {
                    this.showToast('Please select a file first.', 'error');
                    this.hideLoading();
                    return;
                }
                
                const formData = new FormData();
                formData.append('file', this.selectedValidatorFile);
                
                response = await fetch('/api/ats/validate', {
                    method: 'POST',
                    body: formData
                });
            } else {
                const resumeText = document.getElementById('resumeTextArea').value;
                if (!resumeText.trim()) {
                    this.showToast('Please enter resume text.', 'error');
                    this.hideLoading();
                    return;
                }
                
                const formData = new FormData();
                formData.append('resume_text', resumeText);
                
                response = await fetch('/api/ats/validate-text', {
                    method: 'POST',
                    body: formData
                });
            }

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            this.displayValidationResults(result);
            
            this.showToast('ATS validation completed!', 'success');
        } catch (error) {
            console.error('Validation error:', error);
            this.showToast('Error validating resume. Please try again.', 'error');
        } finally {
            this.hideLoading();
        }
    }

    displayValidationResults(result) {
        const resultsDiv = document.getElementById('validationResults');
        resultsDiv.style.display = 'block';

        const validation = result.validation_result;

        // Update score gauge
        const gaugeValue = document.querySelector('.gauge-value');
        gaugeValue.textContent = Math.round(validation.overall_score);
        
        // Update gauge visual
        const gaugeCircle = document.querySelector('.gauge-circle');
        const percentage = validation.overall_score;
        const degrees = (percentage / 100) * 360;
        gaugeCircle.style.background = `conic-gradient(var(--primary-color) ${degrees}deg, var(--border-color) ${degrees}deg)`;

        // Update breakdown bars
        const categories = ['formatting', 'spacing', 'structure'];
        categories.forEach(category => {
            const fill = document.querySelector(`[data-category="${category}"]`);
            if (fill) {
                // Assume each category contributes equally to the score for display
                fill.style.width = `${Math.max(0, percentage - 10 + Math.random() * 20)}%`;
            }
        });

        // Display issues
        const issuesList = document.getElementById('issuesList');
        const allIssues = [
            ...validation.formatting_issues,
            ...validation.spacing_issues,
            ...validation.section_issues,
            ...validation.font_issues
        ];

        if (allIssues.length > 0) {
            issuesList.innerHTML = allIssues.map(issue => `
                <div class="issue-item">${issue}</div>
            `).join('');
        } else {
            issuesList.innerHTML = '<div class="issue-item">No major issues found!</div>';
        }

        // Display recommendations
        const recommendationsList = document.getElementById('recommendationsList');
        recommendationsList.innerHTML = validation.recommendations.map(rec => `
            <div class="recommendation-item">${rec}</div>
        `).join('');

        // Scroll to results
        resultsDiv.scrollIntoView({ behavior: 'smooth' });
    }
}

// Global functions for button actions
window.scrollToSection = function(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
};

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new VibezsumApp();
    
    // Add some easter eggs
    console.log(`
    ✨ Welcome to Vibezsume! ✨
    
    🎯 AI-Powered Resume Analysis
    🛡️ Privacy-First Design
    🚀 Modern Web Technology
    
    Keyboard Shortcuts:
    Ctrl/Cmd + 1 → Home
    Ctrl/Cmd + 2 → Analyzer  
    Ctrl/Cmd + 3 → Builder
    Ctrl/Cmd + 4 → Validator
    
    Built with 💝 for your career success!
    `);
});

// 🎭 Add some fun interactions
document.addEventListener('keydown', (e) => {
    // Konami code easter egg
    if (e.ctrlKey && e.shiftKey && e.key === 'V') {
        const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe'];
        document.documentElement.style.setProperty('--primary-color', colors[Math.floor(Math.random() * colors.length)]);
        app.showToast('🎨 Theme color changed! Keep experimenting!', 'success');
    }
});

// 🌟 Add some visual flair
window.addEventListener('load', () => {
    // Fade in the page
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.8s ease-in-out';
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});
