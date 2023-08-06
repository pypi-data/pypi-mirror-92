//
//                       P r o f i t  S k y  C h e c k . h
//
//  Function:
//     A utility class that checks sky positions for Hector using Profit masks.
//
//  Description:
//     This defines a C++ class, ProfitSkyCheck, that exists to answer the simple
//     question, "can this given Ra,Dec position be used for a sky fibre?" that is,
//     is the specified position clear of any objects - stars, galaxies, etc?.
//     This replaces the original scheme based on the AAO "Cone of Darkness" code,
//     which used TAP requests to the SuperCOSMOS catalogue. Instead, this uses
//     Profit masks, which are FITS files that cover regions of the sky that will
//     be used for HECTOR, and are essentially binary masks - each pixel of the
//     FITS image covers an area of sky (which can be calculated from the WCS
//     coordinate information in the header) and has a zero value of that area
//     of sky is clear and a non-zero value if there this something there.
//
//     This class assumes that there will be a number of such Profit files in
//     a given directory. To initialise the class, it needs to be given the
//     path to this directory, and a range of RA,Dec values. This range should
//     reflect the possible sky fibre positions for the field being configured.
//     The code then checks each file, looking at the WCS information in the
//     header, and notes which files are relevant and the range of sky positions
//     they cover. There is then a querr method that is passed the Ra,Dec of a
//     possible sky fibre, together with a radius for the search, and returns a
//     simple boolean OK/not OK result. If there is anything at all in the relevant
//     Profit file within that radius of that position, this returns false. If it
//     appears clear, it returns true. The code allows for overlap between Profit
//     files, and can check multiple files for the same position, returning a
//     'worst-case' result - ie false if any file shows that area to be
//     contaminated.
//
//     Note that most routines return a boolean function value, which will be
//     true if everything went OK. If there is a problem, this is returned set
//     to false, and a description of the error can be obtained by calling
//     GetError(). In particular, note that the function value returned by
//     CheckUseForSky() is not the result of the test for contamination! The
//     Check argument is used to return the resut of that test.
//
//  Remaining issues: None of this has been tested.
//
//  Author(s): Keith Shortridge, K&V  (Keith@KnaveAndVarlet.com.au)
//
//  History:
//     27th Nov 2020.  Original version.
//      5th Dec 2020. Made the main data array int instead of float. KS.

// ----------------------------------------------------------------------------------

#ifndef __ProfitSkyCheck__
#define __ProfitSkyCheck__

#include <string>
#include <list>
#include <stdlib.h>

#include "ArrayManager.h"

//  There is a structure of type ProfitFileDetails for each file in the directory
//  that is relevant for the current search. Note that it is assumed that all the
//  Profit files have roughtly linear coordinate systems approximately defined by
//  a central Ra,Dec and delta values for each of Ra and Dec. These can then be used
//  as starting points to iterate to a more accurate position if necessary.

struct ProfitFileDetails {
   std::string Path = "";        //  Full file path name.
   int Nx = 0;                   //  Number of pixels in the first (RA) axis
   int Ny = 0;                   //  Number of pixels in the second (Dec) axis
   int** DataArray = NULL;       //  2D Array allocated for the mask data.
   double MidRa = 0.0;           //  RA of the centre of the mask (deg).
   double MidDec = 0.0;          //  Dec of the centre of the mask (deg).
   double DeltaRa = 0.0;         //  Average RA range covered by one pixel (deg).
   double DeltaDec = 0.0;        //  Average Dec range covered by one pixel (deg).
   wcsprm Wcs;                   //  The detailed WCS information for the file.
};

class ProfitSkyCheck {
public:
   //  Constructor
   ProfitSkyCheck (void);
   //  Destructor
   ~ProfitSkyCheck ();
   //  Initialisation
   bool Initialise (const std::string& DirectoryPath, double CentralRaDeg,
                                 double CentralDecDeg, double FieldRadiusDeg);
   //  Querry a potential sky position - Clear returns result of the querry.
   bool CheckUseForSky (double RaDeg, double DecDeg, double RadiusDeg, bool* Clear);
   //  Get description of latest error
   std::string GetError (void) { return I_ErrorText; }
private:
   //  Build up list of files in the mask file directory
   bool GetListOfMaskFiles (void);
   //  Extract Ra,Dec coordinates of image centre from file name.
   bool GetCoordsFromFileName (const std::string& FileName,
                                      double* CenRaDeg, double* CenDecDeg);
   //  Read one of the mask files, checking coordinates and possibly reading data.
   bool ReadAndCheckFile (
      const std::string& MaskFile, double FileRa, double FileDec);
   //  Fix a problem with FITS headers shown by one early mask file example.
   void TidyHeaderFloats(char* HeaderPtr,int NKeys,int* NFixed);
   //  Utility giving Ra,Dec coords and range for a single pixel.
   bool GetPixelDims (wcsprm* WcsPtr,double FIx,double FIy,double* CentreRaDeg,
                  double* CentreDecDeg, double* DeltaRaAsec,double* DeltaDecAsec);
   //  Check for overlap between a mask file area and the field being configured.
   bool FileOverlapsField (
      double MaskCentreRa, double MaskCentreDec, double MaskRaRange,
      double MaskDecRange, double FieldCentreRa, double FieldCentreDec,
      double FieldRadius);
   //  Locate a pixel that contains the specified sky coordinates.
   bool LocatePixFromCoords (ProfitFileDetails& FileDetails,
                        double RaDeg,double DecDeg,int* Ix,int* Iy,bool* Outside);
   //  Format a pair of coordinates in degrees into a string.
   std::string FormatRaDecDeg (double RaDeg, double DecDeg);
   //  Initialisation flag
   bool I_Initialised;
   //  Description of last error, if any.
   std::string I_ErrorText;
   //  The directory holding the Profit files.
   std::string I_DirectoryPath;
   //  The RA centre of the field being checked, in degrees.
   double I_CentralRaDeg;
   //  The Dec centre of the field being checked, in degrees.
   double I_CentralDecDeg;
   //  The radius of the field being checked, in degrees.
   double I_FieldRadiusDeg;
   //  The assumed size of each mask in RA in degrees.
   double I_MaskRaSizeDeg;
   //  The assumed size of each mask in RA in degrees.
   double I_MaskDecSizeDeg;
   //  Used to manage access to multi-dimensional arrays.
   ArrayManager I_ArrayManager;
   //  List of all the full FITS file path names in the mask file directory.
   std::list<std::string> I_MaskFileList;
   //  Details of all the various relevant Profit files.
   std::list<ProfitFileDetails> I_FileDetails;
   //  Any non-fatal warnings generated as the code runs.
   std::list<std::string> I_Warnings;
};

#endif

// ----------------------------------------------------------------------------------

/*                        P r o g r a m m i n g  N o t e s

   o  This assumes the main data array in the ProFit files is integer. It may
      be that the code should check BITPIX and use whatever format is being used
      to avoid unnecessary conversion.
 
*/

