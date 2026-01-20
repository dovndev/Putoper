#!/usr/bin/env python3
"""
Build Script for Auto Typer (Native Version)
Creates distributable packages relying on system dependencies.
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

class AutoTyperBuilder:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.dist_dir = self.project_dir / "dist"
        self.build_dir = self.project_dir / "build"
        self.installer_dir = self.project_dir / "installers"
        self.version = "1.0.0"
        
    def clean(self):
        """Clean previous builds"""
        print("🧹 Cleaning previous builds...")
        for dir_path in [self.dist_dir, self.build_dir, self.installer_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
        print("✅ Clean complete")

    def create_zipapp(self):
        """Create single-file executable using zipapp"""
        print("� Creating Single-File Application...")
        
        self.dist_dir.mkdir(exist_ok=True)
        target = self.dist_dir / "AutoTyper"
        
        # Prepare a temporary directory with files to bundle
        bundle_dir = self.build_dir / "bundle"
        if bundle_dir.exists():
            shutil.rmtree(bundle_dir)
        bundle_dir.mkdir(parents=True)
        
        # Copy source files
        shutil.copy2(self.project_dir / "auto_typing_gtk.py", bundle_dir / "auto_typing_gtk.py")
        shutil.copy2(self.project_dir / "x11_input.py", bundle_dir / "x11_input.py")
        shutil.copy2(self.project_dir / "__main__.py", bundle_dir / "__main__.py")
        
        # Create zipapp
        try:
            subprocess.run([
                sys.executable, "-m", "zipapp",
                str(bundle_dir),
                "-o", str(target),
                "-p", "/usr/bin/env python3",
                "-c"
            ], check=True)
            
            os.chmod(target, 0o755)
            print("✅ Created dist/AutoTyper")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create zipapp: {e}")
            return False

    def create_native_deb(self):
        """Create Debian package for Linux (installing the zipapp)"""
        print("🐧 Creating Native Linux .deb package...")
        
        # Ensure zipapp exists
        if not (self.dist_dir / "AutoTyper").exists():
            if not self.create_zipapp():
                return False
        
        # Create package structure
        pkg_dir = self.build_dir / "auto-typer-deb"
        debian_dir = pkg_dir / "DEBIAN"
        usr_dir = pkg_dir / "usr"
        bin_dir = usr_dir / "bin"
        apps_dir = usr_dir / "share" / "applications"
        
        for dir_path in [debian_dir, bin_dir, apps_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
            
        # Copy ZipApp to /usr/bin/auto-typer
        shutil.copy2(self.dist_dir / "AutoTyper", bin_dir / "auto-typer")
        os.chmod(bin_dir / "auto-typer", 0o755)
        
        # Create control file
        control_content = f'''Package: auto-typer
Version: {self.version}
Section: utils
Priority: optional
Architecture: all
Depends: python3, python3-gi, gir1.2-gtk-3.0, libx11-6, libxtst6
Maintainer: Auto Typer Team <team@autotyper.com>
Description: Modern Text Automation Tool (Native)
 A cross-platform application for automated text typing
 using native system libraries (GTK3 + X11).
'''
        
        with open(debian_dir / "control", "w") as f:
            f.write(control_content)
            
        # Create desktop file
        desktop_content = '''[Desktop Entry]
Name=Auto Typer
Comment=Modern Text Automation Tool
Exec=auto-typer
Icon=input-keyboard
Terminal=false
Type=Application
Categories=Utility;
StartupWMClass=AutoTyper
'''
        
        with open(apps_dir / "auto-typer.desktop", "w") as f:
            f.write(desktop_content)
            
        # Build package
        self.installer_dir.mkdir(exist_ok=True)
        deb_file = self.installer_dir / f"auto-typer_{self.version}_all.deb"
        
        try:
            subprocess.run([
                "dpkg-deb", "--build", str(pkg_dir), str(deb_file)
            ], check=True)
            print("✅ Native Linux .deb package created successfully")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ dpkg-deb not found. Please install dpkg-dev to create .deb packages")
            return False

    def create_portable_zip(self):
        """Create standard zip of the single executable"""
        print("📦 Creating portable zip...")
        
        # Ensure zipapp exists
        if not (self.dist_dir / "AutoTyper").exists():
           self.create_zipapp()
        
        target_zip = self.installer_dir / f"AutoTyper-Linux-Portable.zip"
        
        # We just zip the single file
        with subprocess.Popen(["zip", "-j", str(target_zip), str(self.dist_dir / "AutoTyper")], stdout=subprocess.PIPE) as p:
            p.wait()
            
        print("✅ Portable zip created")
        
    def build_all(self):
        """Build all packages"""
        print("🚀 Starting Auto Typer Native Build...")
        
        self.clean()
        
        self.create_zipapp()
        
        if platform.system() == "Linux":
            self.create_native_deb()
            
        # Also just copy the main app to installers/ for easy access
        self.installer_dir.mkdir(exist_ok=True)
        shutil.copy2(self.dist_dir / "AutoTyper", self.installer_dir / "AutoTyper")
        
        print("\n" + "="*50)
        print("🎉 Build Summary:")
        print("="*50)
        
        if self.installer_dir.exists():
            for file in self.installer_dir.iterdir():
                print(f"✅ {file.name}")
        
        return True

def main():
    """Main entry point"""
    builder = AutoTyperBuilder()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "clean":
            builder.clean()
        elif command == "deb":
            builder.create_native_deb()
        elif command == "portable":
            builder.create_portable_source_archive()
        else:
            print("Usage: python build.py [clean|deb|portable]")
    else:
        builder.build_all()

if __name__ == "__main__":
    main()
