"""MetaMutationalSigs
Usage:
	metaMutatationalSignatures.py --i=<file> [--output=<outdir>] [--genome=<genome>] [--mutationalSignatures] [--sigflow] [--sigfit] [--deconstructSigs]
	metaMutatationalSignatures.py --i=<file> [--output=<outdir>]
	metaMutatationalSignatures.py --browser
	metaMutatationalSignatures.py -h | --help
	metaMutatationalSignatures.py --version
Options:
	--help     Show this screen.
	--version     Show version.
	--i <file>      Input directory with VCF files.
	--output <outdir>		output file path [default: ./metaMutationalSignatures_results.zip/].
	--genome <genome>		genome build, can be GRCh37, GRCh38 [default: GRCh37].
	--browser    Open in browser.
	--mutationalSignatures                   run mutationalSignatures [default: TRUE]. 
	--sigflow                   run sigflow [default: TRUE].  
	--sigfit                   run sigfit [default: TRUE].  
	--deconstructSigs                   run deconstructSigs [default: TRUE].  



   _____          __             _____          __          __  .__                     .__    _________.__              
  /     \   _____/  |______     /     \  __ ___/  |______ _/  |_|__| ____   ____ _____  |  |  /   _____/|__| ____  ______
 /  \ /  \_/ __ \   __\__  \   /  \ /  \|  |  \   __\__  \\   __\  |/  _ \ /    \\__  \ |  |  \_____  \ |  |/ ___\/  ___/
/    Y    \  ___/|  |  / __ \_/    Y    \  |  /|  |  / __ \|  | |  (  <_> )   |  \/ __ \|  |__/        \|  / /_/  >___ \ 
\____|__  /\___  >__| (____  /\____|__  /____/ |__| (____  /__| |__|\____/|___|  (____  /____/_______  /|__\___  /____  >
        \/     \/          \/         \/                 \/                    \/     \/             \/   /_____/     \/ 



Name   :       MetaMutationalSigs
Link   :       https://github.com/PalashPandey/MetaMutationalSigs
Doc    :       https://github.com/PalashPandey/MetaMutationalSigs


"""
from docopt import docopt
import os, time, subprocess, shutil, glob
if __name__ == '__main__':
		arguments = docopt(__doc__, version='MetaMutationalSigs 1.0')
		if arguments["--browser"]:
			os.chdir("flask_ui_app")
			subprocess.call(['python3.8', "app.py"])
		else:
			from SigProfilerMatrixGenerator import install as genInstall
			from SigProfilerMatrixGenerator.scripts import SigProfilerMatrixGeneratorFunc as matGen
			input_dir = arguments["--i"]
			output_dir = arguments["--output"]
			genome_ref = arguments["--genome"]
			runMutationalPatterns = arguments["--mutationalSignatures"]
			runsigflow = arguments["--sigflow"]
			runsigfit = arguments["--sigfit"]
			runDeconstructSigs = arguments["--deconstructSigs"]

			if input_dir ==  None:
				input_dir = "/app/input_vcf_dir"

			if output_dir ==  None:
				output_dir = "/app/input_vcf_dir"

			if genome_ref ==  None:
				genome_ref = "GRCh37"

			if genome_ref ==  "GRCh37":
				# genInstall.install('GRCh37', rsync=False, bash=True)
				genome_ref = "GRCh37"

			if genome_ref ==  "GRCh38":
				# genInstall.install('GRCh38', rsync=False, bash=True)
				genome_ref = "GRCh38"

			if genome_ref ==  "GRCm37":
				genInstall.install('GRCm37', rsync=False, bash=True)
				genome_ref = "GRCm37"

			if genome_ref ==  "GRCm38.p6":
				genInstall.install('GRCm38.p6', rsync=False, bash=True)
				genome_ref = "GRCm38.p6"

			if genome_ref ==  "Rnor_6.0":
				genInstall.install('Rnor_6.0', rsync=False, bash=True)
				genome_ref = "Rnor_6.0"

			if runMutationalPatterns ==  False:
				runMutationalPatterns = "TRUE"

			if runMutationalPatterns ==  True:
				runMutationalPatterns = "FALSE"

			if runsigflow ==  False:
				runsigflow = "TRUE"
			if runsigflow ==  True:
				runsigflow = "FALSE"

			if runsigfit ==  False:
				runsigfit = "TRUE"
			if runsigfit ==  True:
				runsigfit = "FALSE"

			if runDeconstructSigs ==  False:
				runDeconstructSigs = "TRUE"
			if runDeconstructSigs ==  True:
				runDeconstructSigs = "FALSE"
			

			print(input_dir , genome_ref , runMutationalPatterns , runsigflow, runsigfit, runDeconstructSigs)

			matGen.SigProfilerMatrixGeneratorFunc("MetaMutationalSigs", genome_ref , input_dir)
			
			os.chdir("flask_ui_app")
			
			subprocess.call(['Rscript' ,  "../meta_sig_main_flask.r", os.path.join("../" , input_dir ) , genome_ref , runMutationalPatterns , runsigflow, runsigfit, runDeconstructSigs])
			subprocess.call(['python3.8', "../plot_graphs.py", os.path.join("../" , input_dir )   , runMutationalPatterns , runsigflow, runsigfit, runDeconstructSigs])
			

			os.chdir("../")

			print("Current directory " , os.listdir(input_dir))
			print("Current directory " , os.listdir())


			shutil.rmtree(input_dir + "/input" )

			shutil.rmtree(input_dir + "/logs" )
			shutil.rmtree(input_dir + "/output" )

			files_in_directory = os.listdir(input_dir)

			filtered_files = [file for file in files_in_directory if file.endswith(".vcf")]

			shutil.copy("./flask_ui_app/templates/final_results_download.html", input_dir + "/MetaMutationalResults/final_results_download.html")

			shutil.make_archive(output_dir + "/metaMutationalSignatures_results", 'zip', input_dir)

			shutil.rmtree(input_dir +  "/MetaMutationalResults" )
